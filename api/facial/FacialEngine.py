class FacialEngine:

    name = "Base Facial Engine"
    apiKey = ""

    # Load the image repository into the engine (aka API service)
    # type - protocol to use (eg. ftp, http, file, etc)
    # uri - the location to the data. If file, then the uri would be relative path to the files
    def loadRepo(self,type, uri): 
        return true

    # Search for a facial match based on the image provided by the uri parameter
    # type - file or http
    # uri - the location of the file (eg. facialimages/dpd/search/fer2a24s.jpg)
    def search(self,type, uri):  
        return true

    # Callback function that should be used for long running API's
    def searchCallBack(self):
        return true

    # Set the API Key that should be used for accessing the facial API
    # apiKey - the API key for the facial API
    def setAPIKey(self,apiKey):
        self.apiKey = apiKey  

    # Returns the name of the engine
    def getName(self):
        return self.name
    
    # Returns the API Key 
    def getAPIKey(self):
        return self.apiKey
