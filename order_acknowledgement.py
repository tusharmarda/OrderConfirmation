import json
import random
import time

import string_constants as constants
from messageq import MessageQ

class OrderAcknowledgement:
    """This consumer takes "order placed" requests from the queue and sends acknowledgement
    to consumers as SMS and Mail. The mail contains invoice. If invoice is not available,
    send a placeholder mail saying "Invoice will be sent later".
    """
    def __init__(self, q_request, q_sms, q_invoice):
        """Initialize the service with the "order placed" request queue,
        and the message queues for invoices and sms.
        """
        self.q_request = q_request
        self.q_sms = q_sms
        self.q_invoice = q_invoice
        self.consumer_id = 0

    def query_db(self, order_id):
        """Query the database to get the name and SMS number of the customer,
        to format the SMS message.
        """
        time.sleep(1)
        print('Querying DB for acknowledgement of order {}'.format(order_id))
        customer_name = 'abc'
        customer_sms = '1234567890'
        return customer_name, customer_sms

    def process(self, q_message):
        """Process the json message taken from the queue to send requests to send invoice and sms."""
        order_details = json.loads(q_message)
        order_id = order_details[constants.ORDER_ID]

        try:
            order_details[constants.SEND_PLACEHOLDER] = True
            self.q_invoice.enqueue(json.dumps(order_details))

            customer_name, customer_sms = self.query_db(order_id)
            sms_content = ('Dear {}, your Order with order id {} has been '
                + 'successfully placed.').format(customer_name, order_id)
            sms_message = {
                constants.SMS_TO: customer_sms,
                constants.SMS_CONTENT: sms_content,
                constants.SMS_ID: order_id
            }
            self.q_sms.enqueue(json.dumps(sms_message))

            self.q_request.ack(q_message, self.consumer_id)
        except:
            print('Unable to send acknowledgement for order id {}. Will try again.'.format(order_id))

    def listen(self, run_event):
        """Keep polling the message queue endlessly and process any received messages."""
        self.consumer_id = self.q_request.register()
        while run_event.is_set():
            q_message = self.q_request.get_message(self.consumer_id)
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
        self.q_request.deregister(self.consumer_id)
