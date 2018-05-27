from order_acknowledgement import order_acknowledgement
from SMSConsumer import SMSListener
from InvoiceConsumer import InvoiceListener
from EmailConsumer import EmailListener
from collections import deque
from MessageQ import MessageQ
from threading import Thread
from threading import Event
import time
import random
import json



request_q = MessageQ(deque([]))
SmsQ = MessageQ(deque([]))
InvoiceQ = MessageQ(deque([]))
EmailQ = MessageQ(deque([]))

def push_order_requests(run_event):
    for i in range(10):
        request_q.enqueue(json.dumps({'OrderId':('meesho' + str(i))}))
        print('placed order {}.'.format(i))
        time.sleep(random.randint(1, 5))
        if not run_event.is_set():
            break


order_acknowledgement_service = order_acknowledgement(request_q, SmsQ, InvoiceQ)
sms_consumer = SMSListener(SmsQ)
invoice_consumer = InvoiceListener(InvoiceQ, EmailQ)
email_consumer = EmailListener(EmailQ)

interrupt_stop = Event()
interrupt_stop.set()

producer_thread = Thread(target = push_order_requests, args = (interrupt_stop, ))
service_thread = Thread(target = order_acknowledgement_service.listen, args = (interrupt_stop, ))
sms_thread = Thread(target = sms_consumer.listen, args = (interrupt_stop, ))
invoice_thread = Thread(target = invoice_consumer.listen, args = (interrupt_stop, ))
email_thread = Thread(target = email_consumer.listen, args = (interrupt_stop, ))

##try:
producer_thread.start()
service_thread.start()
sms_thread.start()
invoice_thread.start()
email_thread.start()

producer_thread.join()
service_thread.join()
sms_thread.join()
invoice_thread.join()
email_thread.join()
##except:
##    interrupt_stop.clear()
##
##    producer_thread.join()
##    service_thread.join()
##    sms_thread.join()
##    invoice_thread.join()
##    email_thread.join()

    
