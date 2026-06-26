"""
风力发电机仿真专家 — Web 聊天门户
Flask 前端 + Hermes Gateway API 后端

启动: bash start.sh
访问: http://<server-ip>:9997
"""
import json
import requests
from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)

# ── Hermes Gateway API ──
GATEWAY_URL = "http://localhost:8642/v1/chat/completions"
MODEL = "hermes-agent"  # gateway 自动路由

SYSTEM_PROMPT = (
    "你是风力发电机仿真专家。使用中文回答。\n"
    "你精通 OpenFAST / AeroDyn / BEM 求解器 / 气弹耦合 / 叶片设计。\n"
    "代码库位于 /home/mich/LLM/openfast/。\n"
    "回答时引用具体的源文件、行号和物理公式。"
)


@app.route("/")
def index():
    return render_template("index.html",
                           title="🌬️ 风力发电机仿真专家",
                           subtitle="OpenFAST · AeroDyn · BEM · 气弹耦合")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return {"error": "消息不能为空"}, 400

    def generate():
        try:
            resp = requests.post(
                GATEWAY_URL,
                json={
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message},
                    ],
                    "stream": True,
                },
                stream=True,
                timeout=120,
            )

            if resp.status_code != 200:
                yield f"data: {json.dumps({'error': f'Gateway 返回 {resp.status_code}: {resp.text[:200]}'}, ensure_ascii=False)}\n\n"
                return

            for line in resp.iter_lines():
                if not line or line == b"data: [DONE]":
                    continue
                if line.startswith(b"data: "):
                    try:
                        chunk = json.loads(line[6:])
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield f"data: {json.dumps({'text': content}, ensure_ascii=False)}\n\n"
                    except json.JSONDecodeError:
                        pass

            yield f"data: {json.dumps({'done': True})}\n\n"

        except requests.exceptions.ConnectionError:
            yield f"data: {json.dumps({'error': '⚠️ 无法连接 Hermes Gateway (localhost:8642)，请确认 gateway 已启动'}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': f'❌ 错误: {str(e)}'}, ensure_ascii=False)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/health")
def health():
    try:
        r = requests.get("http://localhost:8642/health", timeout=2)
        gw_ok = r.json().get("status") == "ok"
    except Exception:
        gw_ok = False
    return {"status": "ok", "agent": "connected" if gw_ok else "gateway_down"}


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║   🌬️  风力发电机仿真专家 Web 门户            ║")
    print("║   后端: Hermes Gateway API (8642)            ║")
    print("║   访问: http://0.0.0.0:9997                 ║")
    print("╚══════════════════════════════════════════════╝")
    app.run(host="0.0.0.0", port=9997, debug=False, threaded=True)
