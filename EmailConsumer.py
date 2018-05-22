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

    def CallEmailServiceProviderAPI(self, EmailTo, EmailCc, EmailBcc, Subject, Content, Attachment):
        time.sleep(1)
        r = random.randint(0, 1000)
        if r == 0:
            print('Email failed')
            return 0
        print('Email sent')
        return 1

    def getAttachment(self, attachment):
        time.sleep(0.2)
        print('Attachment file acquired')
        return 'Attachment file'

    def deleteFile(self, attachmentFile):
        time.sleep(0.2)
        print('Attachment file deleted')

    def ack(self, qMessage):
        qEmail.pop()

    def process(self, qMessage):
        emailDetails = json.loads(qMessage)
        subject = emailDetails['Subject']
        content = emailDetails['Content']
	emailTo = emailDetails['EmailTo']
	emailCc = ''
	if 'EmailCc' in emailDetails:
            emailCc = emailDetails['EmailCc']
	emailBcc = ''
	if 'EmailBcc' in emailDetails:
            emailBcc = emailDetails['EmailBcc']
	attachmentFile = None
	if 'Attachment' in emailDetails:
            attachment = emailDetails['Attachment']
            if attachment is not None:
                attachmentFile = getAttachment(attachment)
        SentEmail = CallEmailServiceProviderAPI(emailTo, emailCc, emailBcc, subject, content, attachmentFile)
        if SentEmail == 0:
            qEmail.append(qMessage)
        elif attachmentFile is not None:
            deleteFile(attachmentFile)
        ack(qMessage)
