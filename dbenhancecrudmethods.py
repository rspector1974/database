# Import methods
from pymongo import MongoClient
from bson.objectid import ObjectId
import json 

#Create class for interfacing with AAC dabase, including authentication
class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password): # Define __init__ method for authetication
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        self.client = MongoClient('mongodb://%s:%s@localhost:27017' % (username, password))
        self.database = self.client['AAC']

# Complete this create method to implement the C in CRUD.
    def create(self, data):  # Create method to implement the C in CRUD (Create)
        if data is not None: # If data exists
            self.database.animals.insert(data)  #Insert data into database
            return True # Return true if successful
        else:
                return False # Return false if not successful
        if data is None: # If no data is available to pass raise exception
            raise Exception("Nothing to save, because data parameter is empty")
       
    

# Create method to implement the R in CRUD.
    def read(self,read_data): ## define read function
        #if read_data is not None: # if there is data there continue
            readResult = self.database.animals.find(read_data,{"_id":False}) #find data passed to find() function using a projection do not return the _id column from the database.
            return readResult
        #else:
         #   raise Exception("No search criteria has been entered!")# raise expection if no search criteria is available
            
# Create method to print find() results
    def printFind(self,print_data): # define the method to output the record
        #if print_data is not None: # if search criteria exsits 
            if self.database.animals.find(print_data).count() > 0: # If the count of data is greater then 0
                boolean = True # set boolean to true
            else:
                boolean = False # else set boolean to false
            if boolean is True: # if boolen is true output the data to the mydoc variable
                mydoc = self.database.animals.find(print_data) #assign query reuslts to mydoc variable
                for x in mydoc: # iterate through the mydoc variable and return data
                      return x
            else:
                mydoc = ("No data Found") # if boolean is false no data has been found!
                return mydoc
# Create method to implement the U in CRUD.
    def update(self,read_data,update_data): ## define update function
            if self.database.animals.find(read_data).count() > 0:  # if document is found
                boolean = True # set boolean to true
            else: # if document is not found
                 boolean = False # set boolean to false
            if boolean is True: # if document is found
                self.database.animals.update_one(read_data,update_data) #update document
                success_result = self.database.animals.find(read_data) # assign query results to success_results variable
                for x in success_result: # iterate through success_result
                    return x #return x results
            else: # if boolean is false I.E. document not found
                failureMessage = ' Update Failed Document Not Found! ' # assigned Update Failed string to failureMessage                                                                                                            variable
                return failureMessage # return failure message
# Create method to implement the D in CRUD
    def delete(self,read_data): ## define delete function
            if self.database.animals.find(read_data).count() > 0: # if document is found
                boolean = True #set boolean to true
            else: # if document is not found
                boolean = False # set boolean to false
            if boolean is True: # if document is found
                self.database.animals.delete_many(read_data) # delete document
                dict_convert = json.dumps(read_data) # convert dict to string
                success_message = dict_convert + ' Has been deleted' #confirmation notice
                return success_message
            else:
                failureMessage = ' Delete has failed Document Not Found! ' #key pair not found
                return failureMessage
            
                
                
           
            