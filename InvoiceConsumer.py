from collections import deque
import time
import json
import random

class InvoiceListener:
    def __init__(self, invoiceQ, emailQ):
        self.qInvoice = invoiceQ
        self.qEmail = emailQ

    def listen(self):
        if self.qInvoice:
            self.process(self.qInvoice[len(self.qInvoice) - 1])

    def queryDB(self, OrderId):
        time.sleep(1)
        print('Querying DB for Invoice')
        sentInvoice = random.randint(0, 1)
        sentMail = 1
        if sentInvoice == 0:
            sentMail = random.randint(0, 1)
        customerName = 'abc'
        customerEmail = 'abc@def.com'
        invoiceDetails = {'Order No': OrderId, 'Invoice No': random.randint(1, 10000), 'Name': customerName, 'Items':['Item A', 'Item B'], 'Total': (100 * random.randint(1, 100))}
        return sentMail, sentInvoice, customerName, customerEmail, invoiceDetails

    def UpdateDB(self, OrderId, SentMail, SentInvoice):
        time.sleep(1)
        print('Updated DB with values of SentMail and SentInvoice')

    def TryCreateInvoice(self, InvoiceDetails):
        time.sleep(1)
        InvoiceDetailsPath = 'Path of Invoice File created'
        r = random.randint(0, 1000)
        if r == 0:
            return None
        return InvoiceDetailsPath

    def ack(self, qMessage):
        self.qInvoice.pop()

    def process(self, qMessage):
        orderDetails = json.loads(qMessage)
        OrderId = orderDetails['OrderId']
        SentMail, SentInvoice, CustomerName, CustomerEmail, InvoiceDetails = self.queryDB(OrderId)
        if SentInvoice == 0:
            Invoice = self.TryCreateInvoice(InvoiceDetails)
            MailContent = 'Dear ' + CustomerName + ', your order with order id ' + OrderId + ' has been successfully placed.'
            if Invoice is None:
                MailContent += ' Your invoice will be sent in a separate mail.'
            else:
                MailContent += ' Please find your invoice attached to this mail.'
            emailMessage = {'EmailTo': CustomerEmail, 'Subject': 'Your order with Meesho', 'Content': MailContent}
            if Invoice is not None:
                emailMessage['Attachment'] = Invoice
                self.qEmail.append(json.dumps(emailMessage))
                SentInvoice = 1
                SentMail = 1
            elif SentMail == 0:
                self.qEmail.append(json.dumps(emailMessage))
                SentMail = 1
        if SentInvoice == 0:
            self.qInvoice.append(json.dumps(orderDetails))
        self.UpdateDB(OrderId, SentMail, SentInvoice)
        self.ack(qMessage)
