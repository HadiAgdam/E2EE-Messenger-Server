from flask import Flask, request, jsonify
from models import Message
from data import new_message, get_messages_by_time_stamp

app = Flask(__name__)

INVALID_REQUEST_DATA = 400
SUCCESS = 200
INVALID_ARGS = 400


@app.route("/api/new_message", methods=["POST"])
def _new_message():
    data = request.get_json()

    if 'key' in data and 'message' in data and 'time_stamp' in data:
        message = Message(
            key=data.get("json"),
            message=data.get("json"),
            time_stamp=data.get("time_stamp")
        )
        new_message(message)
        return jsonify({
            "status": "success"
        }), SUCCESS
    else:
        return jsonify({
            "error": "invalid request data"
        }), INVALID_REQUEST_DATA


@app.route("/api/get_updates", methods=["GET"])
def _get_updates():
    public_key = request.args.get("p_key")

    if not public_key:
        return jsonify({"error:": "invalid arguments"}), INVALID_ARGS
    last_time_stamp = request.args.get("time_stamp", 0)

    messages = get_messages_by_time_stamp(public_key, last_time_stamp)

    return jsonify(messages), SUCCESS


if __name__ == '__main__':
    app.run()
