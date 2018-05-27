# OrderConfirmation

A dummy project for designing a system to send sms, mail and invoice after order is placed.  
The individual components run as independent microservices to make it scalable.  
If invoice is generated successfully, order mail should have invoice attached, otherwise a footer message "We will send invoice soon" should be present.  
And then the service sends the invoice later when it gets generated.

Created as part of assignment round for Meesho interview.


### To-Do

1. Implement the separate services to run concurrently instead of single sequential calls from Runner.py
2. Clean up code so that it follows Python code conventions