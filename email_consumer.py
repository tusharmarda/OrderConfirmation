import time
import json
import random

from messageq import MessageQ

class EmailListener:
    """This consumer takes email objects from the queue and
    makes external api calls to send the emails.
    """
    def __init__(self, email_q):
        self.email_q = email_q

    def call_email_service_provider_api(
            self, email_to, email_cc, email_bcc,
            subject, content, attachment):
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('Email failed')
            return 0
        print('Email sent')
        return 1

    def get_attachment(self, attachment):
        time.sleep(0.2)
        print('Attachment file acquired')
        return 'Attachment file'

    def delete_file(self, attachment_file):
        time.sleep(0.2)
        print('Attachment file deleted')

    def process(self, q_message):
        email_details = json.loads(q_message)
        subject = email_details['Subject']
        content = email_details['Content']
        email_to = email_details['EmailTo']
        email_cc = ''
        if 'EmailCc' in email_details:
            email_cc = email_details['EmailCc']
        email_bcc = ''
        if 'EmailBcc' in email_details:
            email_bcc = email_details['EmailBcc']
        attachment_file = None
        if 'Attachment' in email_details:
            attachment = email_details['Attachment']
            if attachment is not None:
                attachment_file = self.get_attachment(attachment)
        sent_email = self.call_email_service_provider_api(
            email_to, email_cc, email_bcc,
            subject, content, attachment_file)
        if sent_email == 0:
            self.email_q.enqueue(q_message)
        elif attachment_file is not None:
            self.delete_file(attachment_file)
        self.email_q.ack(q_message)

    def listen(self, run_event):
        while run_event.is_set():
            q_message = self.email_q.get_message()
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
