from MessageQ import MessageQ
import time
import json
import random

class InvoiceListener:
    def __init__(self, invoiceQ, emailQ):
        self.qInvoice = invoiceQ
        self.qEmail = emailQ

    def queryDB(self, OrderId):
        time.sleep(1)
        print('Querying DB for Invoice of order', OrderId)
        sentMail = random.randint(0, 1)
        customerName = 'abc'
        customerEmail = 'abc@def.com'
        invoiceDetails = {'Order No': OrderId, 'Invoice No': random.randint(1, 10000), 'Name': customerName, 'Items':['Item A', 'Item B'], 'Total': (100 * random.randint(1, 100))}
        return sentMail, customerName, customerEmail, invoiceDetails

    def UpdateDB(self, OrderId, SentMail):
        time.sleep(1)
        print('Updated DB with value of SentMail:{}'.format(str(SentMail)))

    def TryCreateInvoice(self, InvoiceDetails):
        time.sleep(1)
        InvoiceDetailsPath = 'Path of Invoice File created'
        r = random.randint(0, 1000)
        if r == 0:
            return None
        return InvoiceDetailsPath

    def process(self, qMessage):
        orderDetails = json.loads(qMessage)
        OrderId = orderDetails['OrderId']
        SentMail, CustomerName, CustomerEmail, InvoiceDetails = self.queryDB(OrderId)
        SentInvoice = 0
        Invoice = self.TryCreateInvoice(InvoiceDetails)
        emailMessage = {'EmailTo': CustomerEmail, 'Subject': 'Your order with Meesho'}
        MailContent = 'Dear ' + CustomerName + ', your order with order id ' + OrderId + ' has been successfully placed.'
        if Invoice is None:
            MailContent += ' Your invoice will be sent in a separate mail.'
        else:
            MailContent += ' Please find your invoice attached to this mail.'
            emailMessage['Attachment'] = Invoice
            SentInvoice = 1
        emailMessage['Content'] = MailContent
        if Invoice is not None or SentMail == 0:
            self.qEmail.enqueue(json.dumps(emailMessage))
            if SentMail == 0:
                SentMail = 1
                self.UpdateDB(OrderId, SentMail)
        if SentInvoice == 0:
            self.qInvoice.enqueue(qMessage)
        self.qInvoice.ack(qMessage)

    def listen(self):
        qMessage = self.qInvoice.getMessage()
        if qMessage is not None:
            self.process(qMessage)
