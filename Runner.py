from SMSConsumer import SMSListener
from InvoiceConsumer import InvoiceListener
from EmailConsumer import EmailListener
from collections import deque
from MessageQ import MessageQ
import json




SmsQ = MessageQ(deque([]))
InvoiceQ = MessageQ(deque([]))
EmailQ = MessageQ(deque([]))

SmsC = SMSListener(SmsQ, InvoiceQ)
InvoiceC = InvoiceListener(InvoiceQ, EmailQ)
EmailC = EmailListener(EmailQ)

for i in range(100):
    SmsQ.enqueue(json.dumps({'OrderId':('meesho' + str(i))}))
    SmsC.listen()
    InvoiceC.listen()
    EmailC.listen()
