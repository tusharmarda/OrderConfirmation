import json
import random
import time

import string_constants as constants
from messageq import MessageQ

class InvoiceListener:
    """This consumer takes requests from the queue and
    creates the invoice for the request.
    If unable to create invoice, it sends a placeholder mail,
    saying that the invoice will be sent later. Then, it
    enqueues the same request again to process later.
    """
    def __init__(self, q_invoice, q_email):
        """Initialize the service with the request queue for invoices, and
        the message queue for the service that sends mails.
        """
        self.q_invoice = q_invoice
        self.q_email = q_email

    def query_db(self, order_id):
        """Query the database to get the details of the order.
        These will be used to create the invoice.
        """
        time.sleep(1)
        print('Querying DB for Invoice of order {}'.format(order_id))
        customer_name = 'abc'
        customer_email = 'abc@def.com'
        invoice_details = {
            'Order No': order_id,
            'Invoice No': random.randint(1, 10000),
            'Name': customer_name,
            'Items': ['Item A', 'Item B'],
            'Total': (100 * random.randint(1, 100))
        }
        order_status = 'placed'
        return customer_name, customer_email, invoice_details, order_status

    def try_create_invoice(self, invoice_details):
        """Try to create a local PDF file of the invoice, and return it's path.
        If unable to create invoice, return None.
        """
        time.sleep(3)
        invoice_details_path = 'Path of Invoice File created'
        r = random.randint(0, 1000)
        if r == 0:
            return None
        return invoice_details_path

    def process(self, q_message):
        """Process the json message taken from the queue to create invoice and send mail."""
        order_details = json.loads(q_message)
        order_id = order_details[constants.ORDER_ID]
        send_placeholder = False
        if constants.SEND_PLACEHOLDER in order_details:
            send_placeholder = order_details[constants.SEND_PLACEHOLDER]
            
        customer_name, customer_email, invoice_details, order_status = self.query_db(order_id)
        invoice = self.try_create_invoice(invoice_details)
        email_message = {
            constants.EMAIL_TO: customer_email,
            constants.EMAIL_SUBJECT: 'Your order with Meesho',
            constants.EMAIL_ID: order_id}
        mail_content = 'Dear {}, your order with order id {} is {}.'.format(customer_name, order_id, order_status)
        if invoice is None:
            mail_content += ' Your invoice will be sent in a separate mail.'
            email_message[constants.EMAIL_ID] += '_NoInvoice'
        else:
            mail_content += ' Please find your invoice attached to this mail.'
            email_message[constants.EMAIL_ATTACHMENTS] = invoice
        email_message[constants.EMAIL_CONTENT] = mail_content

        sent_invoice = False
        if invoice is not None or send_placeholder:
            self.q_email.enqueue(json.dumps(email_message))
            send_placeholder = False
            sent_invoice = invoice is not None
            if sent_invoice:
                print('Invoice sent for order id {}.'.format(order_id))
            else:
                print('Placeholder mail sent for order id {}.'.format(order_id))

        if not sent_invoice:
            order_details[constants.SEND_PLACEHOLDER] = send_placeholder
            self.q_invoice.enqueue(json.dumps(order_details))
        self.q_invoice.ack(q_message)

    def listen(self, run_event):
        """Keep polling the message queue endlessly and process any received messages."""
        while run_event.is_set():
            q_message = self.q_invoice.get_message()
            if q_message is not None:
                self.process(q_message)
            else:
                time.sleep(1)
