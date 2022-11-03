import json, requests, os
from pathlib import Path
from common_lib.pub_sub_client import Subscriber

class GetUserData(Subscriber):
    output_path = './output'
    image_path = os.path.join(output_path, 'images')
    video_path = os.path.join(output_path, 'videos')
    audio_path = os.path.join(output_path, 'audios')
    file_path = os.path.join(output_path, 'files')

    def __init__(self, host, exchange, exchange_type, queue_name, routing_key, access_token):
        Subscriber.__init__(self, host)
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.host = host
        self.access_token =  access_token

    def save_file(self, id: str, content: bytes, msg_type: str, default_file_name: str=''):
        file_name = Path(id)
        if msg_type == 'image':
            file_path = self.image_path
            file_name = file_name.with_suffix('.jpg')
        if msg_type == 'video':
            file_path = self.video_path
            file_name = file_name.with_suffix('.mp4')
        if msg_type == 'audio':
            file_path = self.audio_path
            file_name = file_name.with_suffix('.mp3')

        if msg_type == 'file':
            file_path = self.file_path
            file_name = default_file_name

        final_path = os.path.join(file_path, file_name)
        with open(final_path, "wb") as img_file:
            img_file.write(content)


    def get_contents(self, message: dict):
        events = message['events']

        for event in events:
            msg_id = event['message']['id']
            url = f'https://api-data.line.me/v2/bot/message/{msg_id}/content'
            headers = {'Authorization': f'Bearer {self.access_token}'}
            res = requests.get(url=url, headers=headers)
            
            # save the image
            msg_type = event['message']['type']
            if msg_type == 'image':
                self.save_file(msg_id, res.content, msg_type)

            if msg_type == 'video':
                self.save_file(msg_id, res.content, msg_type)

            if msg_type == 'audio':
                self.save_file(msg_id, res.content, msg_type)
            
            if msg_type == 'file':
                file_name = event['message']['fileName']
                self.save_file(msg_id, res.content, msg_type, file_name)

    def on_message_callback(self, ch, method, properties, body) -> None:
        message = json.loads(body)
        str_msg = json.dumps(message, indent=2)
        print(f'message received:\n{str_msg}')

        self.get_contents(message=message)
        

    def run(self):
        super().setup(exchange=self.exchange, exchange_type=self.exchange_type,
                        queue_name=self.queue_name, routing_key=self.routing_key)
        print('Waiting for message. To exit press Ctrl+C')
        self.channel.start_consuming()