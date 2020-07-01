# coding=utf-8

import os
import sys
sys.path.insert(0,'../common')
sys.path.insert(0,'../orm')

import json
import logging
import time
from medical import Medical
from room_distance import room_distance
from kafkaproducerconsumer import KafkaProducerConsumer

logging.basicConfig(level=logging.INFO)

class MedicalStaff(KafkaProducerConsumer):
    def walk_to_room(self, room):
        logger.info("seeing to patient in room " + room)
        time.sleep(room_distance(room))

    def notify_patient_ready(self, uuid, room):
        logger.info("patient in room " + room + " has been seen to")
        self.notify('patients', {'event': 'patient_treated', 'uuid' : uuid, 'room': room})

    def treat_patient(self):
        logger.info("treating patient")
        time.sleep(10)

    def process(self, message):
        event = json.loads(message.value.decode('utf-8'))
        logger.info("Event: " + str(event))

        self.walk_to_room(event['room'])
        self.treat_patient()
        self.notify_patient_ready(event['uuid'], event['room'])
        self.make_available(Medical, event['name'])

logger = logging.getLogger("medical_staff")
medical_staff = MedicalStaff('medical', 'medical')
medical_staff.monitor_events()