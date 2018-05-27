from order_acknowledgement import order_acknowledgement
from SMSConsumer import SMSListener
from InvoiceConsumer import InvoiceListener
from EmailConsumer import EmailListener
from collections import deque
from MessageQ import MessageQ
import json



request_q = MessageQ(deque([]))
SmsQ = MessageQ(deque([]))
InvoiceQ = MessageQ(deque([]))
EmailQ = MessageQ(deque([]))

order_acknowledgement_service = order_acknowledgement(request_q, SmsQ, InvoiceQ)
SmsC = SMSListener(SmsQ)
InvoiceC = InvoiceListener(InvoiceQ, EmailQ)
EmailC = EmailListener(EmailQ)

for i in range(100):
    request_q.enqueue(json.dumps({'OrderId':('meesho' + str(i))}))
    order_acknowledgement_service.listen()
    SmsC.listen()
    InvoiceC.listen()
    EmailC.listen()
