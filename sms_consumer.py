import json
import random
import time

import string_constants as constants
from messageq import MessageQ

class SMSListener:
    """This consumer takes SMS objects from the queue and
    makes external api calls to send the SMS.
    If unable to do this successfully, it enqueues the same
    message again to process later.
    """
    def __init__(self, smsQ):
        """Initialize listener with a message queue."""
        self.sms_q = smsQ
        self.consumer_id = 0

    def call_sms_service_provider_api(self, sms_to, content, sms_id):
        """Call the API of the external service that sends emails."""
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('Sending SMS {} failed'.format(sms_id))
            return False
        print('SMS {} sent'.format(sms_id))
        return True

    def process(self, q_message):
        """Process the json message taken from the queue to send sms."""
        sms_details = json.loads(q_message)
        content = sms_details[constants.SMS_CONTENT]
        sms_to = sms_details[constants.SMS_TO]
        sms_id = sms_details[constants.SMS_ID]
        sent_sms = self.call_sms_service_provider_api(sms_to, content, sms_id)
        if not sent_sms:
            self.sms_q.enqueue(q_message)
        self.sms_q.ack(q_message, self.consumer_id)

    def listen(self, run_event):
        """Keep polling the message queue endlessly and process any received messages."""
        self.consumer_id = self.sms_q.register()
        while run_event.is_set():
            q_message = self.sms_q.get_message(self.consumer_id)
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
        self.sms_q.deregister(self.consumer_id)
