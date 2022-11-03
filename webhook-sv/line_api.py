from flask import request, jsonify
from flask_restful import Resource
import base64, hashlib, hmac,os
from dotenv import load_dotenv
from common_lib.pub_sub_client import Publisher

load_dotenv('../.env')

LINE_CHANNEL_SECRET=os.environ['LINE_CHANNEL_SECRET']
RABBITMQ_HOST=os.environ['RABBITMQ_HOST']
LINE_WEBHOOK_EXCHANE=os.environ['LINE_WEBHOOK_EXCHANE']
LINE_WEBHOOK_ROUTING_KEY=os.environ['LINE_WEBHOOK_ROUTING_KEY']

class LineApi(Resource):
    def get(self):
        response = jsonify({"message": "Webhook is running..."})
        response.status_code = 200
        return response
    
    def post(self):
        data = request.get_json()
        x_line_sig = request.headers['x-line-signature']
        str_data = request.data.decode('utf-8')
        val_sig = self.validate_signature(LINE_CHANNEL_SECRET, str_data, x_line_sig)

        if val_sig:
            publisher = Publisher(RABBITMQ_HOST)
            publisher.run(LINE_WEBHOOK_EXCHANE, LINE_WEBHOOK_ROUTING_KEY, data)
            response = jsonify(data)
            response.status_code = 200
            return response
        response = jsonify({"message": "Forbidden"})
        response.status_code = 403
        return response
    
    def validate_signature(self, channel_secret: str, body: str, x_line_sig):
        new_hash = hmac.new(channel_secret.encode('utf-8'),
                body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(new_hash).decode('utf-8')
        return x_line_sig == signature
