# coding=utf-8

import os
import sys
import threading
import logging
import json
import uuid
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)

class PatientGenerator:
  __producer = None

  def __init__(self):
    if not os.environ['KAFKA_HOST'] or not os.environ['KAFKA_PORT']:
      sys.exit("KAFKA_HOST and KAFKA_PORT must be configured")

    kafka_url = os.environ['KAFKA_HOST'] + ':' + os.environ['KAFKA_PORT']
    self.__producer = KafkaProducer(bootstrap_servers=[kafka_url])


  def generate_client(self):
    _id = str(uuid.uuid1())
    logger.info("new patient: " + _id)
    event = json.dumps({ 'event' : 'patient_acquisition', 'uuid' : _id })
    self.__producer.send('patients', event.encode('utf-8'))
    threading.Timer(5, self.generate_client, args=None, kwargs=None).start()

logger = logging.getLogger("patients")
generator = PatientGenerator()
generator.generate_client()
