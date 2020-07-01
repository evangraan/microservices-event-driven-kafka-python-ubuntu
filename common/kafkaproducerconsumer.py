import sys
sys.path.insert(0,'../orm')

import os
import json
import threading
from kafka import KafkaConsumer
from kafka import KafkaProducer
from base import Session, engine

class KafkaProducerConsumer:
    __producer = None
    __consumer = None
    __session = None

    def __init__(self, topic, group_id):
        if not os.environ['KAFKA_HOST'] or not os.environ['KAFKA_PORT']:
            sys.exit("KAFKA_HOST and KAFKA_PORT must be configured")

        kafka_url = os.environ['KAFKA_HOST'] + ':' + os.environ['KAFKA_PORT']
        self.__producer = KafkaProducer(bootstrap_servers=kafka_url)
        self.__consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[kafka_url],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            consumer_timeout_ms = 10000)

        self.__session = Session()

    def monitor_events(self):
        for message in self.get_consumer():
            self.process(message)
        threading.Timer(1, self.monitor_events, args=None, kwargs=None).start()

    def get_session(self):
        return self.__session

    def get_producer(self):
        return self.__producer

    def get_consumer(self):
        return self.__consumer

    def make_available(self, clazz, name):
        self.get_session().query(clazz).filter(clazz.name == name).update({"occupied": False})
        self.get_session().commit()

    def make_busy(self, clazz, name):
        self.get_session().query(clazz).filter(clazz.name == name).update({"occupied": True})
        self.get_session().commit()

    def allocate(self, clazz):
        results = self.get_session().query(clazz).filter(clazz.occupied == False)
        if results.count() > 0:
            return results.first().name
        return None

    def get_topic(self, clazz):
        if clazz.__name__ == "Cleaner":
            return "cleaners"
        if clazz.__name__ == "Porter":
            return "porters"
        if clazz.__name__ == "Medical":
            return "medical"
        return "error"

    def dispatch(self, clazz, name, event):
        self.make_busy(clazz, name)
        self.notify(self.get_topic(clazz), event)

    def dispatch_or_wait(self, clazz, uuid, room, reason, dispatch_room, current_room = "none"):
        name = self.allocate(clazz)
        if not name:
            self.ask_to_wait(uuid, room, reason)
        else:
            event = {'event': 'dispatch', 'name' : name, 'room': dispatch_room, 'uuid': uuid, 'current_room' : current_room}
            self.dispatch(clazz, name, event)

    def notify(self, topic, event):
        event = json.dumps(event)
        self.get_producer().send(topic, event.encode('utf-8'))