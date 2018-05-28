# OrderConfirmation

A dummy project for designing a system to send sms, mail and invoice after order is placed.  
The individual components run as independent microservices to make it scalable.  
If invoice is generated successfully, order mail should have invoice attached, otherwise a footer message "We will send invoice soon" should be present.  
And then the service sends the invoice later when it gets generated.

Created as part of assignment round for Meesho interview.


### To-Do

1. Add ability to stop the execution of threads manually
2. Organize output by multiple threads
3. Complete documentation in files