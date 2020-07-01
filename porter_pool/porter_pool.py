# coding=utf-8

import os
import sys
sys.path.insert(0,'../common')
sys.path.insert(0,'../orm')

import json
import time
import logging
from porters import Porter
from room_distance import room_distance
from kafkaproducerconsumer import KafkaProducerConsumer

logging.basicConfig(level=logging.INFO)

class PorterPool(KafkaProducerConsumer):

    def walk_to_room(self, room):
        logger.info("taking patient to " + room)
        time.sleep(room_distance(room))

    def notify_patient_arrival(self, uuid, room):
        logger.info("patient has arrived at " + room)
        self.notify('patients', {'event': 'patient_in_room', 'uuid': uuid, 'room': room})

    def notify_patient_left_room(self, room):
        logger.info("patient has left " + room)
        self.notify('patients', {'event': 'patient_left_room', 'room': room})

    def process(self, message):
        event = json.loads(message.value.decode('utf-8'))
        logger.info("Event: " + str(event))

        self.walk_to_room(event['room'])
        if event['room'] == 'entrance':
            self.notify_patient_left_room(event['current_room'])

        self.notify_patient_arrival(event['uuid'], event['room'])
        self.make_available(Porter, event['name'])

logger = logging.getLogger("porter_pool")
porter_pool = PorterPool('porters', 'porters')
porter_pool.monitor_events()