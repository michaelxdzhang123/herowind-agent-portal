"""密钥管理 - HeroGateway API key management, integrated with main app auth."""

import os
import json
import secrets
import stat
import subprocess
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

from model import db
from utils import auth_login

key_management_bp = Blueprint(
    'key_management_bp',
    __name__,
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_gateway/static'),
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_gateway/templates'),
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GATEWAY_DIR = os.path.join(BASE_DIR, "flask_gateway")
DATA_DIR = os.path.join(GATEWAY_DIR, "data")
KEYS_FILE = os.path.join(DATA_DIR, "keys.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_keys():
    """Load API key records from keys.json."""
    _ensure_data_dir()
    if not os.path.exists(KEYS_FILE):
        return []
    try:
        with open(KEYS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError, OSError):
        return []


def save_keys(keys):
    """Save API key records to keys.json atomically."""
    _ensure_data_dir()
    tmp_file = KEYS_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.chmod(tmp_file, stat.S_IRUSR | stat.S_IWUSR)
    os.replace(tmp_file, KEYS_FILE)


def generate_api_key():
    return "hero_" + secrets.token_urlsafe(32)


def mask_api_key(key):
    if not key or len(key) <= 12:
        return "****"
    return key[:9] + "****************" + key[-4:]


def require_auth():
    """Redirect to main login if not authenticated."""
    if not auth_login():
        return redirect(url_for('login_bp.login_route'))
    return None


@key_management_bp.route("")
def dashboard():
    """密钥管理主页面 - 仅显示当前登录用户的API密钥."""
    redir = require_auth()
    if redir:
        return redir

    # 获取当前登录用户
    current_user = request.cookies.get('username', '')
    is_admin = (current_user in ('admin', 'demo'))

    keys_list = load_keys()
    keys_by_name = {k["name"]: k for k in keys_list}

    user_records = []
    if is_admin:
        for k in keys_list:
            record = {
                "name": k.get("name", ""),
                "api-key": k.get("api-key", ""),
                "api_key_masked": mask_api_key(k.get("api-key", "")),
                "enabled": k.get("enabled", True),
                "display_name": k.get("display_name", ""),
            }
            user_records.append(record)
    else:
        key_record = keys_by_name.get(current_user, {})
        record = {
            "name": current_user,
            "api-key": key_record.get("api-key", ""),
            "api_key_masked": mask_api_key(key_record.get("api-key", "")),
            "enabled": key_record.get("enabled", True) if key_record else False,
            "display_name": key_record.get("display_name", ""),
        }
        user_records.append(record)
        keys_list = [key_record] if key_record.get("api-key") else []

    new_key = session.pop("km_new_key", None)
    new_user = session.pop("km_new_user", None)
    error = session.pop("km_error", None)
    message = session.pop("km_message", None)

    return render_template(
        "users.html",
        users=user_records,
        keys_list=keys_list,
        new_key=new_key,
        new_user=new_user,
        error=error,
        message=message,
    )


@key_management_bp.route("/create", methods=["POST"])
def create_user():
    """为当前登录用户生成API密钥."""
    redir = require_auth()
    if redir:
        return redir

    current_user = request.cookies.get('username', '')
    is_admin = (current_user in ('admin', 'demo'))
    username = request.form.get("username", current_user).strip()
    display_name = request.form.get("display_name", "").strip()

    # 非 admin/demo 不能操作他人密钥
    if not is_admin and username != current_user:
        session["km_error"] = "抱歉，只有ADMIN用户可以使用此功能。"
        return redirect(url_for("key_management_bp.dashboard"))

    keys_list = load_keys()

    # Check if already has a key
    for k in keys_list:
        if k["name"] == username:
            session["km_error"] = f"用户 '{username}' 已有API密钥."
            return redirect(url_for("key_management_bp.dashboard"))

    api_key = generate_api_key()
    new_key_record = {
        "name": username,
        "api-key": api_key,
        "enabled": True,
    }
    if display_name:
        new_key_record["display_name"] = display_name

    keys_list.append(new_key_record)
    save_keys(keys_list)

    session["km_new_key"] = api_key
    session["km_new_user"] = username
    return redirect(url_for("key_management_bp.dashboard"))


@key_management_bp.route("/<name>/delete", methods=["POST"])
def delete_key(name):
    """删除当前用户的API密钥."""
    redir = require_auth()
    if redir:
        return redir

    current_user = request.cookies.get('username', '')
    is_admin = (current_user in ('admin', 'demo'))
    # 非 admin/demo 不能操作他人密钥
    if not is_admin and name != current_user:
        session["km_error"] = "抱歉，只有ADMIN用户可以使用此功能。"
        return redirect(url_for("key_management_bp.dashboard"))

    keys_list = load_keys()
    original_len = len(keys_list)
    keys_list = [k for k in keys_list if k.get("name") != name]
    if len(keys_list) < original_len:
        save_keys(keys_list)
        session["km_message"] = f"已删除用户 '{name}' 的API密钥."
    else:
        session["km_error"] = f"未找到用户 '{name}' 的API密钥."
    return redirect(url_for("key_management_bp.dashboard"))


@key_management_bp.route("/update", methods=["POST"])
def update():
    """运行更新脚本."""
    redir = require_auth()
    if redir:
        return redir

    script_path = os.path.join(GATEWAY_DIR, "update.sh")
    if not os.path.exists(script_path):
        session["km_error"] = "Update script (update.sh) not found."
        return redirect(url_for("key_management_bp.dashboard"))

    try:
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True, text=True, check=True, cwd=GATEWAY_DIR,
        )
        session["km_message"] = "Update completed successfully.\n" + result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        session["km_error"] = "Update script failed.\n" + (exc.stderr.strip() or exc.stdout.strip())
    except OSError as exc:
        session["km_error"] = f"Failed to run update script: {exc}"

    return redirect(url_for("key_management_bp.dashboard"))


@key_management_bp.route("/api/users", methods=["GET"])
def api_users():
    """API: 返回用户和密钥列表（密钥被掩码）."""
    redir = require_auth()
    if redir:
        return jsonify({"error": "Unauthorized"}), 401

    keys_list = load_keys()
    result = []
    for k in keys_list:
        u = dict(k)
        if "api-key" in u:
            u["api-key"] = mask_api_key(u["api-key"])
        result.append(u)
    return jsonify(result)
