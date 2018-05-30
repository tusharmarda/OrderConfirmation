# OrderConfirmation

A dummy project for designing a system to send sms, mail and invoice after order is placed.  
The individual components run as independent microservices to make it scalable.  
If invoice is generated successfully, order mail should have invoice attached, otherwise a footer message "We will send invoice soon" should be present.  
And then the service sends the invoice later when it gets generated.

Created as part of assignment round for Meesho interview.

## Features
1. It has four separate stateless services that run independent of each other. The SMS and Email microservices can be re-used for other purposes, like sending promotional messages.
2. A dummy Message Queue class has been implemented that supports multiple listeners. We can tweak the numbers in runner.py to simulate multiple servers running the same service concurrently, and see the increase in efficiency.


### To-Do

1. Refactor logging to a separate module