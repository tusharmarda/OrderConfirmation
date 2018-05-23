from MessageQ import MessageQ
import time
import json
import random

class SMSListener:
    def __init__(self, smsQ, invoiceQ):
        self.qSMS = smsQ
        self.qInvoice = invoiceQ

    def listen(self):
        qMessage = self.qSMS.getMessage()
        if qMessage is not None:
            self.process(qMessage)

    def queryDB(self, OrderId):
        time.sleep(1)
        print('Querying DB for SMS of order', OrderId)
        sentSMS = random.randint(0, 1)
        sentInvoice = random.randint(0, 1)
        sentMail = 1
        if sentInvoice == 0:
            sentMail = random.randint(0, 1)
        customerName = 'abc'
        customerSMS = '1234567890'
        customerEmail = 'abc@def.com'
        return sentSMS, sentInvoice, customerName, customerSMS

    def updateDB(self, OrderId):
        time.sleep(1)
        print('Updated in DB that SMS is sent for order', OrderId)

    def CallSMSServiceProviderAPI(self, MobileNo, Content):
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('SMS failed')
            return 0
        print('SMS sent')
        return 1

    def process(self, qMessage):
        orderDetails = json.loads(qMessage)
        OrderId = orderDetails['OrderId']
        SentSMS, SentInvoice, CustomerName, CustomerSMS = self.queryDB(OrderId)
        if SentInvoice == 0:
            self.qInvoice.enqueue(json.dumps(orderDetails))
        else:
            print('Invoice for order', OrderId, 'is sent')
        if SentSMS == 0:
            SMSContent = 'Dear ' + CustomerName + ', your Order with order id ' + OrderId + ' has been successfully placed.'
            SentSMS = self.CallSMSServiceProviderAPI(CustomerSMS, SMSContent)
        if SentSMS == 0:
            self.qSMS.enqueue(qMessage)
        else:
            self.updateDB(OrderId)
        self.qSMS.ack(qMessage)
