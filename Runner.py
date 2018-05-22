import SMSConsumer
import InvoiceConsumer
import EmailConsumer
from collections import deque
import json




SmsQ = deque([])
InvoiceQ = deque([])
EmailQ = deque([])

for i in range(100):
    SmsQ.append(json.dumps({'OrderId':('meesho' + str(i))}))

SmsC = SMSConsumer.SMSListener(SmsQ, InvoiceQ)
InvoiceC = InvoiceConsumer.InvoiceListener(InvoiceQ, EmailQ)
EmailC = EmailConsumer.EmailListener(EmailQ)

SmsC.listen()
InvoiceC.listen()
EmailC.listen()
