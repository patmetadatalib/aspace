# aspace
Client for working with REST API for ArchivesSpace


This was a Python client I developed to help with my own work using the REST API for ArchivesSpace. I developed in in order to reduce the amount of time spent wrangling with URLs to access different record types. I also wanted to make it accessible to people just getting into programming like myself, so if you have questions or problems or things that would make it more user-friendly please don't hesitate to contact. 

## INSTALLATION

Install the client using pip
```
pip install aspace
```

### DEPENDENCIES
This client makes use of the [requests](http://docs.python-requests.org/en/master/) library as well as the json library that should ship with Python. It was written using Python 3.6.2 and tested on Windows 10.  

## INITIALIZING THE CLIENT

Initialize the client by passing your username, password, the url of the API, and the repository you would like to work with. 

```
from aspace import Aspace
client = Aspace('uname', 'pword', 'api', repo number)
```		
		
If you are working in the Python interpreter and need to renew your session, use the login() function to retrieve a new session token which will be attached to all subsequent requests.  	

## RENEWING SESSION
```
client.login()
```

## USING THE CLIENT

This client uses separate functions to retrieve different types of records from the API. 

### Retrieving a resource record
To retrieve resources, use the get_resource() record along with the ID of the resource you are looking for.
```
resource_record = client.get_resource(id)

```
Once you have the resource record, you can retrieve the top container for that resource by passing the resource record to the get_resource_tc function. This function will get the ID of the top container and return the JSON for that top container.

```
resource_top_container_record = client.get_resource_tc(resource_record)
```
You can also retrieve the extents and instances in a similar fashion, though these will return the list including the URI rather than the full record.

```
resource_extents = client.get_extents(resource_record)

resource_instance = client.get_instances(resource_record)
```

### Retrieving top containers and archival objects

Functions for retrieving records for an archival object or top container are structured the same way as the functions for resources
```
archival_object = client.get_archival_object(id)
top_container = client.get_container(id)

```

### Working with records
The package has a number of functions for working with any kind of record that can be retrieved from the API.

```
id = client.get_id(record)
```
Given a record, this function returns the ID for any kind of record.

```
field = client.get_field(record, 'field')
```
Given a record and the field name (in quotes) from the JSON model, this function returns the value of taht field or throws an error if the field is not found in the record.

```
updated_record = client.update_record(record, 'field', 'new value')
```
Given a record, the field to be updated, and the new value this function will return an updated record with the new value. NOTE: This function does NOT post the resulting record to the server. To update the record on the server, use the functions below:

### Updating the records in ArchivesSpace 
```
client.update_object(object_record, id)
```
Given  an archival object record and the id for that object, this function sends the updated record to the server and will either return a success message or an error.

```
client.update_resource(resource_record, id)
```
Given a resource record and the id for that object, this function sends the updated record to the server and will either return a success message or an error.

```
client.update_container(container_record, id)
```
Given a top container record and the id for that container, this function sends the updated record to the server and will either return a success message or an error.

