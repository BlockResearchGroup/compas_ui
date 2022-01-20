from compas_cloud import Proxy


class WebApp():

    def __init__(self, app):
        self.app = app
        self.cloud = Proxy()

    def start(self):
        return self.cloud.send({'webapp': {
            'type': 'start'
        }})

    def stop(self):
        return self.cloud.send({'webapp': {
            'type': 'stop'
        }})

    def draw(self, data):
        return self.cloud.send({'webapp': {
            'draw': data
        }})
