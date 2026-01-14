from flask import Flask, jsonify, request
from celery_app import celery
from tasks import send_email, generate_report

app = Flask(__name__)

@app.route("/send-email", methods=["POST"])
def send_email_api():
    data = request.json
    if not all(k in data for k in ("to", "subject", "body")):
        return jsonify({"error": "Missing required fields(to, subject, body)"}), 400
    task = send_email.delay(
        data["to"],
        data["subject"],
        data["body"]
    )

    return jsonify({
        "task_id": task.id,
        "status": "Email task queued"
    }), 202


@app.route("/generate-report", methods=["POST"])
def generate_report_api():
    data = request.json
    if "report_type" not in data:
        return jsonify({"error": "report_type is required"}), 400
    if data["report_type"] not in ["csv", "pdf"]:
        return jsonify({"error": "report_type must be either 'csv' or 'pdf'"}), 400
    task = generate_report.delay(data["report_type"])

    return jsonify({
        "task_id": task.id,
        "status": "Report generation task queued"
    }), 202


@app.route("/task-status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = celery.AsyncResult(task_id)

    return jsonify({
        "task_id": task.id,
        "status": task.status,
        "result": task.result
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
