from flask import Flask, render_template, request, jsonify
from model import get_questions, predict_result
from seed_db import init_db, save_user_result, DB_PATH
import sqlite3
import socket
import qrcode

init_db()

app = Flask(__name__)

questions = get_questions()


@app.route("/")
def intro():
    return render_template("intro.html")


@app.route("/register")
def index():
    return render_template("index.html", questions=questions)


@app.route("/result", methods=["POST"])
def result():
    user_name = request.form.get("user_name", "무명 모험가")

    full_answers = [0.0] * 60

    for i in range(len(questions)):
        raw = request.form.get(f"q{i}")
        if raw is None:
            return render_template("index.html", questions=questions, error="모든 질문에 답해주세요.")
        val = float(raw)
        _, q_idx, _ = questions[i]
        full_answers[q_idx - 1] = val

    res_data = predict_result(full_answers)

    try:
        save_user_result(
            user_name,
            res_data['mbti'],
            res_data['job'],
            res_data['stats']
        )
        print(f"DB 저장 성공: {user_name}")
    except Exception as e:
        print(f"DB 저장 실패: {e}")

    return render_template(
        "result.html",
        result=res_data,
        user_name=user_name,
        party=res_data['party'],
        low_stat_name=res_data['low_stat_name'],
    )


@app.route("/api/party-members")
def party_members_api():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id, name, job, mbti, img_url, atk, mag, holy, dex, lead, sur FROM users ORDER BY name")
        rows = c.fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        print(f"party-members API 오류: {e}")
        return jsonify([])


if __name__ == "__main__":
    port = 8080
    local_ip = socket.gethostbyname(socket.gethostname())
    url = f"http://{local_ip}:{port}"
    qr = qrcode.make(url)
    qr.save("qr.png")
    print(f"\n접속 URL: {url}")
    print(f"QR 코드가 qr.png 로 저장되었습니다.\n")
    app.run(host="0.0.0.0", port=port, debug=False)
