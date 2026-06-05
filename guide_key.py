"""密钥获得 - Guide for obtaining API keys, same as key management."""

import os
import json
import secrets
import stat
import subprocess
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

from model import db, User
from utils import auth_login

guide_key_bp = Blueprint(
    'guide_key_bp',
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
    if not auth_login():
        return redirect(url_for('login_bp.login_route'))
    return None


@guide_key_bp.route("/guide_key")
def dashboard():
    """密钥获得主页面."""
    redir = require_auth()
    if redir:
        return redir

    users_list = User.query.all()
    keys_list = load_keys()
    keys_by_name = {k["name"]: k for k in keys_list}
    user_records = []
    for user in users_list:
        key_record = keys_by_name.get(user.username, {})
        record = {
            "name": user.username,
            "api-key": key_record.get("api-key", ""),
            "api_key_masked": mask_api_key(key_record.get("api-key", "")),
            "enabled": key_record.get("enabled", True) if key_record else False,
            "display_name": key_record.get("display_name", ""),
        }
        user_records.append(record)

    new_key = session.pop("gk_new_key", None)
    new_user = session.pop("gk_new_user", None)
    error = session.pop("gk_error", None)
    message = session.pop("gk_message", None)

    return render_template(
        "guide_key.html",
        users=user_records,
        new_key=new_key,
        new_user=new_user,
        error=error,
        message=message,
    )


@guide_key_bp.route("/guide_key/create", methods=["POST"])
def create_user():
    """为已存在的数据库用户生成API密钥."""
    redir = require_auth()
    if redir:
        return redir

    username = request.form.get("username", "").strip()
    display_name = request.form.get("display_name", "").strip()

    user = User.query.filter_by(username=username).first()
    if not user:
        session["gk_error"] = f"用户 '{username}' 不存在于用户表中."
        return redirect(url_for("guide_key_bp.dashboard"))

    keys_list = load_keys()
    for k in keys_list:
        if k["name"] == username:
            session["gk_error"] = f"用户 '{username}' 已有API密钥."
            return redirect(url_for("guide_key_bp.dashboard"))

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

    session["gk_new_key"] = api_key
    session["gk_new_user"] = username
    return redirect(url_for("guide_key_bp.dashboard"))


@guide_key_bp.route("/guide_key/<name>/delete", methods=["POST"])
def delete_key(name):
    """删除用户的API密钥."""
    redir = require_auth()
    if redir:
        return redir

    keys_list = load_keys()
    original_len = len(keys_list)
    keys_list = [k for k in keys_list if k.get("name") != name]
    if len(keys_list) < original_len:
        save_keys(keys_list)
        session["gk_message"] = f"已删除用户 '{name}' 的API密钥."
    else:
        session["gk_error"] = f"未找到用户 '{name}' 的API密钥."
    return redirect(url_for("guide_key_bp.dashboard"))
