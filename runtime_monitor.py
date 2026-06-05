"""运行监控 - Runtime log viewer for VLLM run logs."""

import os
from flask import Blueprint, render_template, request, jsonify

from utils import auth_login

runtime_monitor_bp = Blueprint('runtime_monitor_bp', __name__)

# Default log file path, configurable via environment variable
DEFAULT_LOG_FILE = os.environ.get(
    "VLLM_RUN_LOG_FILE",
    "/home/mich/LLM/vlm/vlm_run.log",
)

# Max lines to read at once
MAX_LINES = 500
# Max file size to display (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024


def require_auth():
    if not auth_login():
        from flask import redirect, url_for
        return redirect(url_for('login_bp.login_route'))
    return None


@runtime_monitor_bp.route("/runtime_monitor", methods=["GET"])
def runtime_monitor_route():
    """运行监控页面 - 显示VLLM运行日志."""
    redir = require_auth()
    if redir:
        return redir

    log_file = request.args.get("log_file", DEFAULT_LOG_FILE)
    num_lines = int(request.args.get("lines", MAX_LINES))
    if num_lines < 1:
        num_lines = 1
    if num_lines > 2000:
        num_lines = 2000

    log_content = ""
    log_info = {}
    error_msg = None

    if not os.path.exists(log_file):
        error_msg = f"日志文件不存在: {log_file}"
        log_info["path"] = log_file
        log_info["exists"] = False
    else:
        file_size = os.path.getsize(log_file)
        log_info["path"] = log_file
        log_info["exists"] = True
        log_info["size"] = file_size
        log_info["size_human"] = _human_size(file_size)
        log_info["lines"] = num_lines

        if file_size > MAX_FILE_SIZE:
            error_msg = f"文件过大 ({_human_size(file_size)}), 最大支持 {_human_size(MAX_FILE_SIZE)}"
        elif file_size == 0:
            log_content = "(日志文件为空)"
        else:
            try:
                log_content = _tail_file(log_file, num_lines)
            except PermissionError:
                error_msg = f"无权限读取: {log_file}"
            except OSError as e:
                error_msg = f"读取失败: {e}"

    return render_template(
        "runtime_monitor.html",
        log_content=log_content,
        log_info=log_info,
        error_msg=error_msg,
        log_file=log_file,
        num_lines=num_lines,
    )


@runtime_monitor_bp.route("/runtime_monitor/refresh", methods=["GET", "POST"])
def runtime_monitor_refresh():
    """刷新日志内容."""
    redir = require_auth()
    if redir:
        return redir

    log_file = request.form.get("log_file", request.args.get("log_file", DEFAULT_LOG_FILE))
    num_lines = int(request.form.get("lines", request.args.get("lines", MAX_LINES)))

    return runtime_monitor_route()


@runtime_monitor_bp.route("/runtime_monitor/api", methods=["GET"])
def runtime_monitor_api():
    """API接口: 返回日志尾部内容."""
    redir = require_auth()
    if redir:
        return jsonify({"error": "Unauthorized"}), 401

    log_file = request.args.get("log_file", DEFAULT_LOG_FILE)
    num_lines = int(request.args.get("lines", 100))

    if not os.path.exists(log_file):
        return jsonify({"error": f"文件不存在: {log_file}"}), 404

    try:
        content = _tail_file(log_file, min(num_lines, 2000))
        return jsonify({"path": log_file, "lines": content.split("\n")})
    except OSError as e:
        return jsonify({"error": str(e)}), 500


def _tail_file(filepath, n):
    """Read the last n lines from a file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        # Go to end and read backwards to find n lines
        f.seek(0, 2)
        file_size = f.tell()
        if file_size == 0:
            return ""

        lines_found = []
        line_start = file_size
        buffer = ""

        # Read backwards to find n line boundaries
        bytes_to_check = min(file_size, n * 200)  # assume avg 200 bytes per line
        f.seek(max(0, file_size - bytes_to_check))
        chunk = f.read()
        all_lines = chunk.split("\n")

        # Take last n lines
        result = all_lines[-n:] if len(all_lines) > n else all_lines
        return "\n".join(result)


def _human_size(size_bytes):
    """Convert bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
