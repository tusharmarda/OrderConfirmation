from collections import deque
import time
import json
import random

qSMS = deque([])
qInvoice = deque([])
qEmail = deque([])

class EmailListener:
    qEmail = deque([])
    def __init__(self, emailQ):
        self.qEmail = emailQ

class InvoiceListener:
    qInvoice = deque([])
    def __init__(self, invoiceQ):
        self.qInvoice = invoiceQ

class SMSListener:
    emptyQ = 0
    def __init__(self, smsQ, invoiceQ):
        self.qSMS = smsQ
        self.qInvoice = invoiceQ

    def listen(self):
        if qSMS:
            process(qSMS.pop())

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
