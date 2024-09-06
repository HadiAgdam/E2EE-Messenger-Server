from flask import Flask, request, jsonify
from models import Message
from data import new_message, get_messages_by_id
import re

app = Flask(__name__)

INVALID_REQUEST_DATA = 400
SUCCESS = 200
INVALID_ARGS = 400


def is_valid_public_key(public_key):
    if public_key.startswith("04") and len(public_key) == 130:
        return re.match(r'^[0-9a-fA-F]{130}$', public_key) is not None
    elif public_key.startswith(("02", "03")) and len(public_key) == 66:
        return re.match(r'^[0-9a-fA-F]{66}$', public_key) is not None
    return False


@app.route("/api/new_message", methods=["POST"])
def _new_message():
    data = request.get_json()

    if 'receiver' in data and 'key' in data and 'message' in data:
        if not is_valid_public_key(data['receiver']):
            return jsonify({"error": "Invalid ECC public key"}), INVALID_REQUEST_DATA

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
            "error": "Invalid request data"
        }), INVALID_REQUEST_DATA


@app.route("/api/get_message", methods=["GET"])
def _get_updates():
    try:
        public_key = request.args.get("p_key")

        if not public_key or not is_valid_public_key(public_key):
            return jsonify({"error": "invalid arguments"}), INVALID_ARGS

        last_id = request.args.get("message_id", 0)

        try:
            last_id = int(last_id)
        except ValueError:
            return jsonify({"error": "message_id must be an integer"}), INVALID_ARGS

        messages = get_messages_by_id(public_key, last_id)
        return jsonify(messages), SUCCESS

    except Exception as e:
        return jsonify({"error": str(e)}), INVALID_REQUEST_DATA


if __name__ == '__main__':
    app.run()
