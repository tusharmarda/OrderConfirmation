from collections import deque

qSMS = deque([])
qInvoice = deque([])
qEmail = deque([])

class EmailListener:
    qEmail = deque([])

class SMSListener:
    qURL = ''
    def __init__(self, URL):
        qURL = URL
        
