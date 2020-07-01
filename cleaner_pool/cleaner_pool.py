# coding=utf-8

import os
import sys
sys.path.insert(0,'../common')
sys.path.insert(0,'../orm')

import json
import logging
import time
from cleaners import Cleaner
from room_distance import room_distance
from kafkaproducerconsumer import KafkaProducerConsumer

logging.basicConfig(level=logging.INFO)

class CleanerPool(KafkaProducerConsumer):
    def walk_to_room(self, room):
        logger.info("About to clean " + room)
        time.sleep(room_distance(room))

    def clean_room(self):
        logger.info("cleaning room")
        time.sleep(9)

    def notify_cleaned_room(self, room):
        logger.info("Cleaned room " + room)
        self.notify('patients', {'event': 'room_cleaned', 'room': room})

    def process(self, message):
        event = json.loads(message.value.decode('utf-8'))
        logger.info("Event: " + str(event))

        self.walk_to_room(event['room'])  # one direction
        self.clean_room()

        self.notify_cleaned_room(event['room'])
        self.make_available(Cleaner, event['name'])

logger = logging.getLogger("cleaner_pool")
cleaner_pool = CleanerPool('cleaners', 'cleaners')
cleaner_pool.monitor_events()