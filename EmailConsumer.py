from collections import deque
import time
import json
import random


class EmailListener:
    def __init__(self, emailQ):
        self.qEmail = emailQ


    def listen(self):
        if qEmail:
            process(qEmail[len(qEmail) - 1])

    def CallEmailServiceProviderAPI(self, EmailTo, EmailCc, EmailBcc, Content, Attachment):
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('Email failed')
            return 0
        print('Email sent')
        return 1

    def ack(self, qMessage):
        qEmail.pop()

    def process(self, qMessage):
        emailDetails = json.loads(qMessage)
	emailTo = emailDetails['EmailTo']
	emailCc = ''
	if 'EmailCc' in emailDetails:
            emailCc = emailDetails['EmailCc']
	emailBcc = ''
	if 'EmailBcc' in emailDetails:
            emailBcc = emailDetails['EmailBcc']
	content = ''
	if 'Content' in emailDetails:
            content = emailDetails['Content']
	attachmentFile = None
	if 'Attachment' in emailDetails:
            attachment = emailDetails['Attachment']
            attachmentFile = getAttachment(attachment)
        SentEmail = CallEmailServiceProviderAPI(emailTo, emailCc, emailBcc, content, attachmentFile)
        if SentEmail == 0:
            qEmail.append(qMessage)
        ack(qMessage)
