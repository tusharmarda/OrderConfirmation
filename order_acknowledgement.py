from MessageQ import MessageQ
import time
import json
import random
import threading

class order_acknowledgement:
    def __init__(self, requestQ, smsQ, invoiceQ):
        self.qRequest = requestQ
        self.qSMS = smsQ
        self.qInvoice = invoiceQ

    def query_db(self, OrderId):
        time.sleep(1)
        print('Querying DB for acknowledgement of order {}'.format(OrderId))
        sentSMS = random.randint(0, 1)
        sentInvoice = random.randint(0, 1)
        customerName = 'abc'
        customerSMS = '1234567890'
        customerEmail = 'abc@def.com'
        return sentSMS, sentInvoice, customerName, customerSMS

    def update_db(self, OrderId):
        time.sleep(1)
        print('Updated in DB that SMS is sent for order', OrderId)

    def process(self, q_message):
        orderDetails = json.loads(q_message)
        OrderId = orderDetails['OrderId']
        SentSMS, SentInvoice, CustomerName, CustomerSMS = self.query_db(OrderId)
        if SentInvoice == 0:
            self.qInvoice.enqueue(json.dumps(orderDetails))
        else:
            print('Invoice for order', OrderId, 'is sent')
        if SentSMS == 0:
            SMSContent = 'Dear {}, your Order with order id {} has been successfully placed.'.format(CustomerName, OrderId)
            sms_message = {'SmsTo': CustomerSMS, 'SMSContent':SMSContent}
            self.qSMS.enqueue(json.dumps(sms_message))
            SentSMS = 1
            self.update_db(OrderId)
        self.qRequest.ack(q_message)

    def listen(self, run_event):
        while run_event.is_set():
            qMessage = self.qRequest.getMessage()
            if qMessage is not None:
                self.process(qMessage)
            else:
                time.sleep(1)
