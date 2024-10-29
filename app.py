from flask import Flask, request, jsonify
from models import Message
from data import new_message, get_messages_by_id


app = Flask(__name__)

INVALID_REQUEST_DATA = 400
SUCCESS = 200
INVALID_ARGS = 400
SERVER_ERROR = 400


def is_valid_public_key(public_key):
    # if public_key.startswith("04") and len(public_key) == 130:
    #     return re.match(r'^[0-9a-fA-F]{130}$', public_key) is not None
    # elif public_key.startswith(("02", "03")) and len(public_key) == 66:
    #     return re.match(r'^[0-9a-fA-F]{66}$', public_key) is not None
    # return False
    return True


@app.route("/api/new_message", methods=["POST"])
def _new_message():
    data = request.json

    if 'receiver' in data and 'encryptionKey' in data and 'encryptedMessage' in data and 'iv' in data:
        if not is_valid_public_key(data['receiver']):
            return jsonify({"error": "Invalid ECC public key"}), INVALID_REQUEST_DATA

        if new_message(encryption_key=data.get('encryptionKey'),
                       encrypted_message=data.get('encryptedMessage'),
                       iv=data.get('iv'),
                       recipient_public_key=data.get('receiver')):
            return jsonify({"status": "success"}), SUCCESS
        else:
            return jsonify({
                "status": "server error"
            }), SERVER_ERROR
    else:
        return jsonify({
            "error": "Invalid request data"
        }), INVALID_REQUEST_DATA


@app.route("/api/get_message", methods=["GET"])
def _get_updates():
    try:
        public_key = request.args.get("publicKey")
        last_id = request.args.get("messageId", 0)

        if not public_key or not is_valid_public_key(public_key):
            return jsonify({"error": "invalid arguments"}), INVALID_ARGS

        try:
            last_id = int(last_id)
        except ValueError:
            return jsonify({"error": "message_id must be an integer"}), INVALID_ARGS

        messages = get_messages_by_id(public_key, last_id)
        result = []

        for message in messages:
            result.append({
                "messageId": message.message_id,
                "encryptionKey": message.encryption_key,
                "encryptedMessage": message.encrypted_message,
                "time": message.time,
                "iv": message.iv
            })
        return jsonify(result), SUCCESS

    except Exception as e:
        return jsonify({"error": str(e)}), INVALID_REQUEST_DATA


