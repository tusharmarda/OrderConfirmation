import json
import random
import time
from collections import deque
from threading import Event, Thread

from email_consumer import EmailListener
from invoice_consumer import InvoiceListener
from messageq import MessageQ
from order_acknowledgement import OrderAcknowledgement
from sms_consumer import SMSListener

def push_order_requests(request_q, run_event):
	"""Send "Order placed" requests to the message queue that our service is listening to."""
	for i in range(100):
		request_q.enqueue(json.dumps({'OrderId': ('meesho' + str(i))}))
		print('Placed order {}.'.format(i))
		time.sleep(random.randint(0, 500) / 100)
		if not run_event.is_set():
			break

def run(request_q, order_acknowledgement_service, sms_consumer, 
		invoice_consumer, email_consumer, interrupt_stop):
	"""This is the main runner function. It triggers all the different consumer on different threads."""
	producer_thread = Thread(
		target = push_order_requests,
		args = (request_q, interrupt_stop,))
	service_thread = Thread(
		target = order_acknowledgement_service.listen,
		args = (interrupt_stop,))
	sms_thread = Thread(
		target = sms_consumer.listen,
		args = (interrupt_stop,))
	invoice_thread = Thread(
		target = invoice_consumer.listen,
		args = (interrupt_stop,))
	email_thread = Thread(
		target = email_consumer.listen,
		args = (interrupt_stop,))

	try:
		producer_thread.start()
		service_thread.start()
		sms_thread.start()
		invoice_thread.start()
		email_thread.start()
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
	   interrupt_stop.clear()
	finally:
	   producer_thread.join()
	   service_thread.join()
	   sms_thread.join()
	   invoice_thread.join()
	   email_thread.join()
	print('Simulation complete.')

def main():
	"""Initialize and trigger all message queues and their listeners."""
	request_q = MessageQ(deque([]))
	sms_q = MessageQ(deque([]))
	invoice_q = MessageQ(deque([]))
	email_q = MessageQ(deque([]))

	order_acknowledgement_service = OrderAcknowledgement(
		request_q, sms_q, invoice_q)
	sms_consumer = SMSListener(sms_q)
	invoice_consumer = InvoiceListener(invoice_q, email_q)
	email_consumer = EmailListener(email_q)

	stop_event = Event()
	stop_event.set()
    
	run(request_q, order_acknowledgement_service, sms_consumer,
		invoice_consumer, email_consumer, stop_event)

main()