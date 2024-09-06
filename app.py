from flask import Flask, request, jsonify
from models import Message
from data import new_message, get_messages_by_id

app = Flask(__name__)

INVALID_REQUEST_DATA = 400
SUCCESS = 200
INVALID_ARGS = 400


@app.route("/api/new_message", methods=["POST"])
def _new_message():
    data = request.get_json()

    if 'receiver' in data and 'key' in data and 'message' in data:
        message = Message(
            receiver=data.get("receiver"),
            key=data.get("key"),
            message=data.get("message"),
        )
        new_message(message)
        return jsonify({
            "status": "success"
        }), SUCCESS
    else:
        return jsonify({
            "error": "invalid request data"
        }), INVALID_REQUEST_DATA


@app.route("/api/get_message", methods=["GET"])
def _get_updates():
    public_key = request.args.get("p_key")

    if not public_key:
        return jsonify({"error:": "invalid arguments"}), INVALID_ARGS

    last_id = request.args.get("message_id", 0)

    messages = get_messages_by_id(public_key, last_id)

    return jsonify(messages), SUCCESS


if __name__ == '__main__':
    app.run()
