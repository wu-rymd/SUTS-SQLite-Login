# SUTS-SQLite-Login
Flask web application as proof-of-concept for simple SQLite database manipulation using user registrations and log-ins


* * *


###### `v1.1.0`
Add hashing functionality for sensitive information using `hashlib` module 
* Database stores hashed registration password entry 
  * Increased security
* Authorizes user log-in by comparing hashed log-in password entry and hashed database password entry 
 
`hashlib` [Documentation](https://docs.python.org/2/library/hashlib.html)


* * *


###### `v1.0.0`
Basic data manipulation using user login/registration
* Duplicate e-mail addresses cannot be registered 
* Runs locally
