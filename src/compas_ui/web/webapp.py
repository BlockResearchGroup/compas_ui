from compas_cloud import Proxy
from uuid import uuid4
import time


class WebApp():

    def __init__(self, app):
        self.app = app
        self.cloud = Proxy()
        self.webapp_id = None

    def start(self):
        result = self.cloud.send({'webapp': {
            'type': 'start',
            'webapp_id': str(uuid4())
        }})
        self.webapp_id = result['webapp_id']

        print("Waiting for webapp to start...")
        while True:
            time.sleep(0.2)
            if self.check():
                break
        print("Webapp started!")

        for guid in self.app.scene.nodes:
            self.app.scene.nodes[guid].draw()

    def check(self):
        response = self.cloud.send({'webapp': {
            'type': 'check',
            'webapp_id': self.webapp_id
        }})

        if response:
            return response['registered']

    def stop(self):
        return self.cloud.send({'webapp': {
            'type': 'stop'
        }})

    def draw(self, data):
        if self.check():
            return self.cloud.send({'webapp': {
                'type': 'draw',
                'webapp_id': self.webapp_id,
                'data': data
            }})
