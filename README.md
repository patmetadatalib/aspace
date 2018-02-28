# aspace
Client for working with REST API for ArchviesSpace


This was a client I developed to help with my own work using the REST API for ArchivesSpace. I developed in in order to reduce the amount of time spent wrangling with URLs to access different record types. 

INITIALIZING THE CLIENT
		>>>from aspace import Aspace
		>>>client = Aspace('uname', 'pword', 'api', repo number)
		
		
		
		
	RENEWING SESSION
		>>>client.login()
