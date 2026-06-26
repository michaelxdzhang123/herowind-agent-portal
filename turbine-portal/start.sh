#!/bin/bash
# ============================================================
# 风力发电机仿真专家 — Web 门户启动脚本
# 使用 Hermes 自带的 venv（包含所有依赖）
#
# 启动: bash start.sh
# 停止: Ctrl+C
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "╔══════════════════════════════════════════════╗"
echo "║   🌬️  风力发电机仿真专家 Web 门户            ║"
echo "║   模型: deepseek-v4-pro                      ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# 使用 Hermes 的 venv（所有依赖已安装）
HERMES_VENV="/home/mich/LLM/vscode/hermes-agent/.venv"
source "$HERMES_VENV/bin/activate"

# 设置 PYTHONPATH
export PYTHONPATH="/home/mich/LLM/vscode/hermes-agent:$PYTHONPATH"

# 检查并安装缺失依赖
python -c "import openai, dotenv, flask, requests" 2>/dev/null || {
    echo "安装缺失依赖..."
    pip install openai python-dotenv flask requests --quiet
}

# 显示访问地址
IP=$(hostname -I 2>/dev/null | awk '{print $1}')
echo "  ┌─────────────────────────────────────────┐"
echo "  │  内网访问:  http://${IP:-localhost}:9999  │"
echo "  └─────────────────────────────────────────┘"
echo ""
echo "  按 Ctrl+C 停止"
echo ""

cd "$SCRIPT_DIR"
python app.py
