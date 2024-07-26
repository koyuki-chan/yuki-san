import os
from dotenv import load_dotenv
import json

class Config:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        load_dotenv(os.path.join(self.BASE_DIR, '.env'))
        self.SESSDATA = os.getenv('SESSDATA')
        self.TOKEN = os.getenv('TOKEN')
        self._load_json_config('config.json')

    def _load_json_config(self, filepath):
        with open(os.path.join(self.BASE_DIR, filepath), 'r') as f:
            json_config = json.load(f)
            self.UID= json_config.get('uid')
            self.ROOM_ID= json_config.get('room_id')
            self.CHANNEL_ID = json_config.get('channel_ID')

config = Config()