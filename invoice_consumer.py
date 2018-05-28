import time
import json
import random

from messageq import MessageQ

class InvoiceListener:
    def __init__(self, q_invoice, q_email):
        self.q_invoice = q_invoice
        self.q_email = q_email

    def query_db(self, order_id):
        time.sleep(1)
        print('Querying DB for Invoice of order', order_id)
        sent_mail = random.randint(0, 1)
        customer_name = 'abc'
        customer_email = 'abc@def.com'
        invoice_details = {
            'Order No': order_id,
            'Invoice No': random.randint(1, 10000),
            'Name': customer_name,
            'Items': ['Item A', 'Item B'],
            'Total': (100 * random.randint(1, 100))
        }
        return sent_mail, customer_name, customer_email, invoice_details

    def update_db(self, order_id, sent_mail):
        time.sleep(1)
        print('Updated DB with value of SentMail:{}'.format(str(sent_mail)))

    def try_create_invoice(self, invoice_details):
        time.sleep(1)
        invoice_details_path = 'Path of Invoice File created'
        r = random.randint(0, 1000)
        if r == 0:
            return None
        return invoice_details_path

    def process(self, q_message):
        order_details = json.loads(q_message)
        order_id = order_details['OrderId']
        sent_mail, customer_name, customer_email, invoice_details = self.query_db(order_id)
        sent_invoice = 0
        invoice = self.try_create_invoice(invoice_details)
        email_message = {'EmailTo': customer_email, 'Subject': 'Your order with Meesho'}
        mail_content = 'Dear {}, your order with order id {} has been successfully placed.'.format(customer_name, order_id)
        if invoice is None:
            mail_content += ' Your invoice will be sent in a separate mail.'
        else:
            mail_content += ' Please find your invoice attached to this mail.'
            email_message['Attachment'] = invoice
            sent_invoice = 1
        email_message['Content'] = mail_content
        if invoice is not None or sent_mail == 0:
            self.q_email.enqueue(json.dumps(email_message))
            if sent_mail == 0:
                sent_mail = 1
                self.update_db(order_id, sent_mail)
        if sent_invoice == 0:
            self.q_invoice.enqueue(q_message)
        self.q_invoice.ack(q_message)

    def listen(self, run_event):
        while run_event.is_set():
            q_message = self.q_invoice.get_message()
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
