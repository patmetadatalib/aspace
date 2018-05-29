# aspace
Python client for working with REST API for ArchivesSpace



## INSTALLATION

Install the client using pip
```
pip install aspace
```

#### DEPENDENCIES
This client makes use of the [requests](http://docs.python-requests.org/en/master/) library as well as the json library that should ship with Python. It was written using Python 3.6.2 and tested on Windows 10.  

## INITIALIZING THE CLIENT

Initialize the client by passing your username, password, the url of the API, and the repository you would like to work with. All but the repo number should be wrapped in quotes. Though setups may differ, this client assumes there will be no slash at the end of the API URL and will add the relevant directory structure depending on the type of operation you are performing.  

```
from aspace import Aspace
client = Aspace('uname', 'pword', 'api', repo number)
```		
### RENEWING SESSION 		
If you are working in the Python interpreter and need to renew your session, use the login() function to retrieve a new session token which will be attached to all subsequent requests.  	

```
client.login()
```

## USING THE CLIENT

This client uses separate functions to retrieve different types of records from the API. I used descriptive names for the variables here, but in practice I typically use much shorter ones (e.g. a single letter for the client, 'tc' for top container, etc.)

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

#### Getting Record ID
```
id = client.get_id(record)
```
Given a record, this function returns the ID for any kind of record.

#### Getting a field from a record

```
field = client.get_field(record, 'field')
```
Given a record and the field name (in quotes) from the JSON model, this function returns the value of that field or throws an error if the field is not found in the record.

#### Updating a field on an existing record

```
updated_record = client.change_record(record, 'field', 'new value')
```
Given a record, the field to be updated, and the new value this function will return an updated record with the new value. NOTE: This function does NOT post the resulting record to the server. This also means that controlled value fields, which differ from institution to institution, are also not checked at this stage so while any new value can be added here, it will throw an error once sent to the server. 
UPDATE: the name of this function has been changed from update_record to change_record in order to clarify differences between changing the record and posting those changes to the server. 
To update the record on the server, use the functions below:

### Updating the records in ArchivesSpace 

#### Updating an object
```
client.update_object(object_record, id)
```
Given  an archival object record and the id for that object, this function sends the updated record to the server and will either return a success message or an error.

#### Updating a resource

```
client.update_resource(resource_record, id)
```
Given a resource record and the id for that object, this function sends the updated record to the server and will either return a success message or an error.

#### Updating a top container

```
client.update_container(container_record, id)
```
Given a top container record and the id for that container, this function sends the updated record to the server and will either return a success message or an error.


### Searching repositories via API 

As of version 1.5 I have added functions to help with searching a repository via the API. The client currently utilzes a function for performing a keyword search and a separate function for particular fields. Some fields may not be searchable, but that should be refleced in the results. 

#### Performing a search

These functions take a search term and return a list of all records returned by the server in JSON. If a search will return more than 100 pages of records (default is 10 records per page), the user will be prompted whether they would like to perform the search or abandon it. 
##### Keyword search
```
search_term = 'Union'
results = client.keyword_search(search_term)
```
##### Title (or other field search)
```
search_term = 'Union'
field = 'title'
results = client.field_search(search_term, field)

```

#### Analyzing results
This function will take the results of the search function above and return a Python dictionary of records where the key is the record type and the value for that key is the list of all records of that type. It will also print a list of all record types found in the search and the number of records for each type. 

For example:

```
results_dict = client.analyze_results(results)

```

will produce
```
[('archival_objects', 400), ('corporate_entities', 7), ('resources', 34), ('people', 2)]
```
and allow you to perform functions on the results_dict dictionary as you would any other dictionary. The records are stored in JSON format. NOTE: the current version is not able to send changes made to these results back to the server as updates. 

### Writing finding aids and other descriptions to a file
This client also allows you to make use of built-in functions in ArchivesSpace to write EAD and MARC descriptions of resources in various file formats. Since the generation of finding aids and other record types takes place on the server, there isn't a way to alter the way ArchivesSpace develops the file using this client. It also means that this client cannot write these files using records that have been changed if those changes are not reflected on the server. 

Currently ArchivesSpace can create EAD, EAD3, and MARC records for a given resource. Both versions of EAD can be written as PDF files or XML files, though the MARC record will only be written in XML. Regardless of the desired format, the functions take an id of a resource and the desired file name and will write the files to the current directory. Examples of how each function works are shown below:

```
id = 1017
client.write_ead(id, 'ead') => ~/Current_Folder/ead.xml
client.write_ead_pdf(id, 'ead_pdf' => ~/Current_Folder/ead_pdf.pdf

client.write_ead3(id, 'ead3') => ~/Current_Folder/ead3.xml
client.write_ead3_pdf(id, 'ead3_pdf') => ~/Current_Folder/ead3_pdf.pdf

client.write_marc(id, 'marc') => ~/Current_Folder/marc.xml



```



## ABOUT

This was a Python client I developed to help with my own work using the REST API for ArchivesSpace. I developed in in order to reduce the amount of time spent wrangling with URLs to access different record types. I also wanted to make it accessible to people just getting into programming like myself. I'm still trying to get my head around git but if you have ideas to make this more helpful please do so through pull requests and as long as they work that works for me. 

Since this was developed to help with my own work I plan to update it with new functions as I need them or as new features become available on ArchivesSpace, though there is no schedule for those updates. If I make changes I will make sure they are reflected in [PYPI](https://pypi.python.org/pypi/aspace/1.3) as well. The most recent published version is 1.5 

### Known Problems 
Check the known problems page for a list of bugs I've come across in the package but haven't fixed. If you come across other problems please contact me via email so I can hopefully address them or at least acknowledge them there so others are aware. 

A common problem that I run into is not doing a JSON dump of a record I've changed before sending it back to the server. When I get more time I'd like to automatically check for this in the client or do it by default, but in case others run into problems that's something to try. Read more here: https://docs.python.org/3/library/json.html

Contact me at 

harringp [at] uwosh.edu
