#!/bin/bash
# ============================================================
# 风力发电机仿真专家 — 诊断测试脚本
# 运行: bash test_portal.sh
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

pass()  { echo -e "  ${GREEN}✅ PASS${NC}  $1"; }
fail()  { echo -e "  ${RED}❌ FAIL${NC}  $1"; }
warn()  { echo -e "  ${YELLOW}⚠️  WARN${NC}  $1"; }
info()  { echo -e "  ${CYAN}ℹ️  INFO${NC}  $1"; }
step()  { echo -e "\n${CYAN}─── $1 ───${NC}"; }

echo "╔══════════════════════════════════════════════╗"
echo "║  🌬️  Turbine Portal 诊断测试                  ║"
echo "╚══════════════════════════════════════════════╝"

ERRORS=0

# ── 1. 检查文件 ──
step "1. 检查项目文件"
for f in app.py templates/index.html start.sh; do
    if [ -f "$f" ]; then
        pass "$f 存在"
    else
        fail "$f 缺失"
        ERRORS=$((ERRORS+1))
    fi
done

# ── 2. 检查 Python 和依赖 ──
step "2. 检查 Python 环境"
HERMES_VENV="/home/mich/LLM/vscode/hermes-agent/venv"
HERMES_SRC="/home/mich/LLM/vscode/hermes-agent"

if [ -f "$HERMES_VENV/bin/python" ]; then
    PYTHON="$HERMES_VENV/bin/python"
    pass "Hermes venv Python: $PYTHON"
else
    fail "Hermes venv 不存在: $HERMES_VENV"
    ERRORS=$((ERRORS+1))
    PYTHON=python3
fi

# 检查关键模块
for mod in flask dotenv; do
    if $PYTHON -c "import $mod" 2>/dev/null; then
        pass "Python 模块 $mod"
    else
        fail "Python 模块 $mod 缺失 — 安装: $PYTHON -m pip install $mod"
        ERRORS=$((ERRORS+1))
    fi
done

# ── 3. 检查 Hermes Agent 能否导入 ──
step "3. 检查 AIAgent 导入"
AIAGENT_OK=false
if PYTHONPATH="$HERMES_SRC:$PYTHONPATH" $PYTHON -c "
import os; os.environ['HERMES_HOME'] = os.path.expanduser('~/.hermes')
from dotenv import load_dotenv; load_dotenv(os.path.expanduser('~/.hermes/.env'))
from run_agent import AIAgent
print('AIAgent imported OK')
" 2>&1; then
    pass "AIAgent 导入成功"
    AIAGENT_OK=true
else
    fail "AIAgent 导入失败（见上方错误）"
    ERRORS=$((ERRORS+1))
fi

# ── 4. 检查 API 密钥 ──
step "4. 检查 DeepSeek API 密钥"
if grep -q "DEEPSEEK_API_KEY" ~/.hermes/.env 2>/dev/null; then
    pass "DEEPSEEK_API_KEY 已配置"
else
    fail "DEEPSEEK_API_KEY 未配置"
    ERRORS=$((ERRORS+1))
fi

# ── 5. 端口检查 ──
step "5. 检查端口占用"
for port in 5000; do
    if ss -tlnp 2>/dev/null | grep -q ":$port "; then
        PID=$(ss -tlnp 2>/dev/null | grep ":$port " | sed -n 's/.*pid=\([0-9]*\).*/\1/p' | head -1)
        warn "端口 $port 已被占用 (PID: $PID)"
        info "如果需要释放: kill $PID"
    else
        pass "端口 $port 空闲"
    fi
done

# ── 6. 如果 AIAgent 可用，做全链路测试 ──
if [ "$AIAGENT_OK" = true ]; then
    step "6. 全链路测试（Flask 启动 → API 调用 → 响应验证）"

    TMP_LOG=$(mktemp)

    # 启动 Flask 在后台
    info "启动 Flask..."
    cd "$(dirname "$0")"
    export PYTHONPATH="$HERMES_SRC:$PYTHONPATH"
    $PYTHON app.py > "$TMP_LOG" 2>&1 &
    FLASK_PID=$!

    # 等待就绪（最多15秒）
    READY=false
    for i in $(seq 1 15); do
        if curl -s http://127.0.0.1:5000/health >/dev/null 2>&1; then
            READY=true
            pass "Flask 已就绪 (${i}s)"
            break
        fi
        sleep 1
    done

    if [ "$READY" = false ]; then
        fail "Flask 启动超时 — 日志:"
        cat "$TMP_LOG"
        kill $FLASK_PID 2>/dev/null
        ERRORS=$((ERRORS+1))
    else
        # ── 测试 HTML 页面 ──
        info "测试 HTML 页面..."
        HTML=$(curl -s http://127.0.0.1:5000/ 2>&1)
        if echo "$HTML" | grep -q "风力发电机仿真专家"; then
            pass "HTML 页面正常返回"
        else
            fail "HTML 页面异常"
            ERRORS=$((ERRORS+1))
        fi

        # 检查 CDN 依赖
        if echo "$HTML" | grep -q "cdn.jsdelivr.net"; then
            fail "HTML 仍有 CDN 依赖（内网不可用）"
            ERRORS=$((ERRORS+1))
        else
            pass "HTML 无 CDN 依赖"
        fi

        # ── 测试 API 调用 ──
        info "测试 API 调用（提问: 1+1等于几）..."
        RESP=$(curl -s -X POST http://127.0.0.1:5000/api/chat \
            -H "Content-Type: application/json" \
            -d '{"message":"1+1等于几？用一句话回答","session_id":"test_diag"}' 2>&1)

        if echo "$RESP" | grep -q '"text"'; then
            pass "API 返回文本响应"
            # 提取回答
            ANSWER=$(echo "$RESP" | python3 -c "
import sys,json
for line in sys.stdin:
    if line.startswith('data: '):
        d = json.loads(line[6:])
        if 'text' in d: print(d['text'][:200])
" 2>/dev/null)
            if [ -n "$ANSWER" ]; then
                info "回答内容: $ANSWER"
            fi
        elif echo "$RESP" | grep -q '"error"'; then
            fail "API 返回错误: $(echo "$RESP" | grep 'error')"
            ERRORS=$((ERRORS+1))
        else
            fail "API 无有效响应 — 原始内容: ${RESP:0:200}"
            info "Flask 日志:"
            cat "$TMP_LOG" | tail -20
            ERRORS=$((ERRORS+1))
        fi
    fi

    # 清理
    kill $FLASK_PID 2>/dev/null || true
    rm -f "$TMP_LOG"
else
    warn "跳过全链路测试（AIAgent 不可用）"
fi

# ── 总结 ──
echo -e "\n══════════════════════════════════════════════"
if [ "$ERRORS" -eq 0 ]; then
    echo -e "${GREEN}✅ 所有测试通过！可以运行: bash start.sh${NC}"
else
    echo -e "${RED}❌ 发现 $ERRORS 个问题，请修复后重试${NC}"
fi
echo "══════════════════════════════════════════════"
