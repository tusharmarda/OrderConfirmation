import json
import random
import time

from messageq import MessageQ

class EmailListener:
    """This consumer takes email objects from the queue and
    makes external api calls to send the emails.
    If unable to do this successfully, it enqueues the same
    message again to process later.
    """
    def __init__(self, email_q):
        """Initialize listener with a message queue."""
        self.email_q = email_q

    def call_email_service_provider_api(
            self, email_to, email_cc, email_bcc,
            subject, content, attachment, email_id):
        """Call the API of the external service that sends emails."""
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('Sending email {} failed'.format(email_id))
            return False
        print('Email {} sent'.format(email_id))
        return True

    def get_attachment(self, attachment):
        """Create a local copy of the Attachment files."""
        time.sleep(0.2)
        print('Attachment file acquired')
        return 'Attachment file'

    def delete_file(self, attachment_file):
        """Delete the copy of attachment file that was used to send api call."""
        time.sleep(0.2)
        print('Attachment file deleted')

    def process(self, q_message):
        """Process the json message taken from the queue to send mail."""
        email_details = json.loads(q_message)
        subject = email_details['Subject']
        content = email_details['Content']
        email_to = email_details['EmailTo']
        email_id = email_details['EmailId']
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
            subject, content, attachment_file, email_id)
        if not sent_email:
            self.email_q.enqueue(q_message)
        elif attachment_file is not None:
            self.delete_file(attachment_file)
        self.email_q.ack(q_message)

    def listen(self, run_event):
        """Keep polling the message queue endlessly and process any received messages."""
        while run_event.is_set():
            q_message = self.email_q.get_message()
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
