# coding=utf-8

import sys
sys.path.insert(0,'../orm')
sys.path.insert(0,'../common')

import json
import logging
from waiting import Waiting
from patients import Patient
from porters import Porter
from medical import Medical
from room import Room
from cleaners import Cleaner
from kafkaproducerconsumer import KafkaProducerConsumer

logging.basicConfig(level=logging.INFO)

class HospitalAdministration(KafkaProducerConsumer):
    def process(self, message):
        event = json.loads(message.value.decode('utf-8'))
        logger.info("event is: [" + str(event) + "]")

        self.process_acquisition(event)
        self.process_patient_room_arrival(event)
        self.process_patient_treated(event)
        self.process_room_cleaned(event)
        self.process_patient_left_room(event)
        self.process_waiting()

    def process_acquisition(self, event):
        if event['event'] == 'patient_acquisition':
            room = self.allocate(Room)
            porter = self.allocate(Porter)
            if not room:
                self.refer_patient(event['uuid'])
            else:
                self.make_busy(Room, room)

                if porter:
                    self.book_patient(event['uuid'], room)
                    self.dispatch(Porter, porter, {'event': 'dispatch', 'name': porter, 'room': room, 'uuid': event['uuid'], 'current_room': 'none'})
                else:
                    self.ask_to_wait(event['uuid'], room, 'porter')

    def process_patient_room_arrival(self, event):
        if event['event'] == 'patient_in_room':
            if event['room'] == 'entrance':
                self.discharge_patient(event['uuid'])
            else:
                self.dispatch_or_wait(Medical, event['uuid'], event['room'], 'medical', event['room'])

    def process_patient_treated(self, event):
        if event['event'] == 'patient_treated':
            self.dispatch_or_wait(Porter, event['uuid'], event['room'], 'treated', 'entrance', event['room'])

    def process_room_cleaned(self, event):
        if event['event'] == 'room_cleaned':
            self.make_available(Room, event['room'])

    def process_patient_left_room(self, event):
        if event['event'] == 'patient_left_room' and event['room'] != 'entrance':
            self.dispatch_or_wait(Cleaner, 'none', event['room'], 'cleaner', event['room'])

    def process_waiting(self):
        entries = self.get_session().query(Waiting).all()

        for waiting in entries:
            self.process_waiting_for_cleaner(waiting)
            self.process_waiting_for_medical(waiting)
            self.process_waiting_for_porter(waiting)

    def process_waiting_for_cleaner(self, waiting):
        if waiting.waiting_for == 'cleaner':
            cleaner = self.allocate(Cleaner);
            if cleaner:
                self.dispatch(Cleaner, cleaner, {'event': 'dispatch', 'name': cleaner, 'room': waiting.room})

    def process_waiting_for_medical(self, waiting):
        if waiting.waiting_for == 'medical':
            medical = self.allocate(Medical);
            if medical:
                self.Dispatch(Medical, medical,
                              {'event': 'dispatch', 'name': medical, 'room': waiting.room, 'uuid': waiting.patient})

    def process_waiting_for_portr(self, waiting):
        if waiting.waiting_for == 'porter':
            porter = self.allocate(Porter);
            if porter:
                self.dispatch(Porter, porter,
                              {'event': 'dispatch', 'name': porter, 'room': waiting.room, 'uuid': waiting.patient,
                               'current_room': 'none'})

    def refer_patient(self, patient):
        logger.info("no more room - refer patient to another hospital")
        patient = Patient(patient, 'referred', True)
        self.get_session().commit()

    def discharge_patient(self, uuid):
        logger.info("patient " + uuid + " discharged")
        self.get_session().query(Patient).filter(Patient.uuid == uuid).update({"released": True})
        self.get_session().commit()

    def ask_to_wait(self, uuid, room, waiting_for):
        logger.info("asking " + uuid + " to wait on " + room + " for "  + waiting_for)
        waiting = Waiting(uuid, room, waiting_for)
        self.get_session().commit()

    def book_patient(self, uuid, room):
        logger.info("patient booked in - dispatching porter")
        patient = Patient(uuid, room, False)
        logger.info("Selected room [" + room + "]")
        self.get_session().commit()

logger = logging.getLogger("hospital_administration")
hospital_administration = HospitalAdministration('patients', 'hospital')
hospital_administration.monitor_events()
