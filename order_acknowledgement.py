import time
import json
import random

from messageq import MessageQ

class OrderAcknowledgement:
    def __init__(self, q_request, q_sms, q_invoice):
        self.q_request = q_request
        self.q_sms = q_sms
        self.q_invoice = q_invoice

    def query_db(self, order_id):
        time.sleep(1)
        print('Querying DB for acknowledgement of order {}'.format(order_id))
        sent_sms = random.randint(0, 1)
        sent_invoice = random.randint(0, 1)
        customer_name = 'abc'
        customer_sms = '1234567890'
        return sent_sms, sent_invoice, customer_name, customer_sms

    def update_db(self, order_id):
        time.sleep(1)
        print('Updated in DB that SMS is sent for order', order_id)

    def process(self, q_message):
        order_details = json.loads(q_message)
        order_id = order_details['OrderId']
        sent_sms, sent_invoice, customer_name, customer_sms = self.query_db(order_id)
        if sent_invoice == 0:
            self.q_invoice.enqueue(json.dumps(order_details))
        else:
            print('Invoice for order', order_id, 'is sent')
        if sent_sms == 0:
            SMSContent = ('Dear {}, your Order with order id {} has been '
                + 'successfully placed.').format(customer_name, order_id)
            sms_message = {'SmsTo': customer_sms, 'SMSContent':SMSContent}
            self.q_sms.enqueue(json.dumps(sms_message))
            sent_sms = 1
            self.update_db(order_id)
        self.q_request.ack(q_message)

    def listen(self, run_event):
        while run_event.is_set():
            q_message = self.q_request.get_message()
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
