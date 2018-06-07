## Known bugs/to be fixed:

* get_id functions throws error when reading records saved in lists in the Python interpreter. Probably affects the other record-independent functions
* update_resource record throws an error if the record has been edited in Python. This is usually solved by doing a JSON dump of the updated record, which can then be sent to the server along with the resource ID. 
* When changing lots of records via the API, you can create a mismatch between the SQL database and the Solr index. This is especially problematic for the public interface. I'm going to try and re-work the update functions for better batch support in a way that might address this problem and update the client accordingly. 

## In Progress

## TO DO
* working with agents/subjects
* editing results of search and updating them 
* Better batch processing support 
