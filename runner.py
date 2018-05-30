import json
import random
import time
from collections import deque
from threading import Event, Thread

import string_constants as constants
from email_consumer import EmailListener
from invoice_consumer import InvoiceListener
from messageq import MessageQ
from order_acknowledgement import OrderAcknowledgement
from sms_consumer import SMSListener

request, sms, invoice, email = 0, 1, 2, 3

def push_order_requests(request_q, run_event):
	"""Send "Order placed" requests to the message queue that our service is listening to."""
	for i in range(100):
		request_q.enqueue(json.dumps({constants.ORDER_ID: ('meesho' + str(i))}))
		print('Placed order {}.'.format(i))
		time.sleep(random.randint(0, 1) / 100)
		if not run_event.is_set():
			break

def run(message_queues, consumers, interrupt_stop):
	"""This is the main runner function. It triggers all the different consumers on different threads."""
	threads = []
	for i in range(4):
		cleanup_thread = Thread(
		target = message_queues[i].cleanup_stragglers,
		args = (interrupt_stop,))
		threads.append(cleanup_thread)

		for consumer in consumers[i]:
			listener_thread = Thread(
			target = consumer.listen,
			args = (interrupt_stop,))
			threads.append(listener_thread)

	producer_thread = Thread(
		target = push_order_requests,
		args = (message_queues[request], interrupt_stop,))
	threads.append(producer_thread)

	start_time = time.time()
	try:
		for t in threads:
			t.start()
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		interrupt_stop.clear()
		print('Closing all threads safely.')
	finally:
		for t in threads:
			t.join()
	end_time = time.time()
	print('Simulation complete in {} minutes.'.format((end_time - start_time) / 60))

def main():
	"""Initialize and trigger all message queues and their listeners."""
	message_queues = []
	for i in range(4):
		message_queues.append(MessageQ(deque([])))
	consumers = [[] for i in range(4)]

	# These numbers simulate the number of various consumers to the queue.
	# Tweak these to see the performance difference
	num_request_consumers = 10
	num_sms_consumers = 10
	num_invoice_consumers = 25
	num_email_consumers = 10

	for i in range(num_request_consumers):
		order_acknowledgement_service = OrderAcknowledgement(
			message_queues[request],
			message_queues[sms],
			message_queues[invoice])
		consumers[request].append(order_acknowledgement_service)
	
	for i in range(num_sms_consumers):
		sms_consumer = SMSListener(message_queues[sms])
		consumers[sms].append(sms_consumer)
	
	for i in range(num_invoice_consumers):
		invoice_consumer = InvoiceListener(
			message_queues[invoice],
			message_queues[email])
		consumers[invoice].append(invoice_consumer)
	
	for i in range(num_email_consumers):
		email_consumer = EmailListener(message_queues[email])
		consumers[email].append(email_consumer)

	stop_event = Event()
	stop_event.set()
    
	run(message_queues, consumers, stop_event)

main()