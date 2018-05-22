from collections import deque
import time
import json
import random

class SMSListener:
    def __init__(self, smsQ, invoiceQ):
        self.qSMS = smsQ
        self.qInvoice = invoiceQ

    def listen(self):
        if qSMS:
            process(qSMS[len(qSMS) - 1])

    def queryDB(self, OrderId):
        time.sleep(1)
        print('Querying DB')
        sentSMS = random.randint(0, 1)
        sentInvoice = random.randint(0, 1)
        sentMail = 1
        if sentInvoice == 0:
            sentMail = random.randint(0, 1)
        customerName = 'abc'
        customerSMS = '1234567890'
        customerEmail = 'abc@def.com'
        return sentSMS, sentMail, sentInvoice, customerName, customerSMS, customerEmail

    def updateDB(self, OrderId):
        time.sleep(1)
        print('Updated in DB that SMS is sent')

    def CallSMSServiceProviderAPI(self, MobileNo, Content):
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('SMS failed')
            return 0
        print('SMS sent')
        return 1

    def ack(self, qMessage):
        qSMS.pop()

    def process(self, qMessage):
        orderDetails = json.loads(qMessage)
        OrderId = orderDetails['OrderId']
        SentSMS, SentMail, SentInvoice, CustomerName, CustomerSMS, CustomerEmail = queryOrder(OrderId)
        if SentInvoice == 0:
            orderDetails['SentInvoice'] = SentInvoice
            orderDetails['SentMail'] = SentMail
            orderDetails['CustomerName'] = CustomerName
            orderDetails['CustomerEmail'] = CustomerEmail
            qInvoice.append(json.dumps(orderDetails))
        if SentSMS == 0:
            SMSContent = 'Dear ' + CustomerName + ', your Order with order id ' + OrderId + ' has been successfully placed.'
            SentSMS = CallSMSServiceProviderAPI(CustomerSMS, SMSContent)
        if SentSMS == 0:
            qSMS.append(qMessage)
        else:
            updateDB(OrderId)
        ack(qMessage)
