import time
import json
import random

from messageq import MessageQ

class SMSListener:
    """This consumer takes SMS objects from the queue and
    makes external api calls to send the SMS.
    """
    def __init__(self, smsQ):
        self.sms_q = smsQ

    def call_sms_service_provider_api(self, sms_to, content):
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('SMS failed')
            return 0
        print('SMS sent')
        return 1

    def process(self, q_message):
        sms_details = json.loads(q_message)
        content = sms_details['SMSContent']
        sms_to = sms_details['SmsTo']
        sent_sms = self.call_sms_service_provider_api(sms_to, content)
        if sent_sms == 0:
            self.sms_q.enqueue(q_message)
        self.sms_q.ack(q_message)

    def listen(self, run_event):
        while run_event.is_set():
            q_message = self.sms_q.get_message()
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
