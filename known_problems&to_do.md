## Known bugs/to be fixed:

* get_id functions throws error when reading records saved in lists in the Python interpreter. Probably affects the other record-independent functions
* update_resource record throws an error if the record has been edited in Python. This is usually solved by doing a JSON dump of the updated record, which can then be sent to the server along with the resource ID. 

## In Progress

## TO DO
* working with agents/subjects
* editing results of search and updating them 
