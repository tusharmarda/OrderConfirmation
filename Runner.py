import SMSConsumer
import InvoiceConsumer
import EmailConsumer
from collections import deque


SmsQ = deque([])
InvoiceQ = deque([])
EmailQ = deque([])

SmsC = SMSConsumer.SMSListener(SmsQ, InvoiceQ)
InvoiceC = InvoiceConsumer.InvoiceListener(InvoiceQ, EmailQ)
EmailC = EmailConsumer.EmailListener(EmailQ)

SmsC.listen()
InvoiceC.listen()
EmailC.listen()
