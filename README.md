# Petstore API

## To Build
```
docker build -t petstore .
docker run --name=petstore -d -p 5000:5000 petstore:latest
```

## Purpose
This is a vulnerable by design API.  It is very poorly coded to test and see how vulnerabilities can exist in APIs.  It has been designed after the Swagger Pet Store API.  It uses the same schema and endpoints. 

## Flaws Reported
 - SQL Injection
 - Command Injection
 - Local File Inclusion/Read

## User Endpoints
|VERB|ENDPOINT|DESC|NOTES|
|----|---|---|---|
|GET |/user/\<username>   |Retrieve a single user  by username|   |
|GET |/user   |Retrieve all users   |   |
|POST|/user   |Create a user|   |
|POST|/user/login   |Retrieve an auth token|   |
|POST|/user/logout   |Logout user|   |
|PUT|/user/\<username>   |Update a user by username|   |
|DELETE|/user/\<username>   |Delete a user by username|   |


## Admin Endpoints
|VERB|ENDPOINT|DESC|NOTES|
|----|---|---|---|
|GET|/admin/log?logFile=log_1.log|View current log file|LFI|
|POST|/admin/run/uptime|View server uptime|Command Injection|



## Pet Endpoints
|VERB|ENDPOINT|DESC|NOTES|
|----|---|---|---|
|POST|/pet|Add a new pet||
|PUT|/pet|Update and existing pet||
|GET|/pet/findByStatus|Find pet by status||
|GET|/pet/\<petId>|Retrieve pet by Id||
|DELETE|/pet/\<petId>|Deletes a pet by Id||

## Store Endpoints
|VERB|ENDPOINT|DESC|NOTES|
|----|---|---|---|
|GET|/store/inventory|Display store inventory||
|POST|/store/order|Create an order||
|GET|/store/order/\<orderId>|Retrieve an order by Id||
|DELETE|/store/order/\<orderId>|Delete an order by Id||
