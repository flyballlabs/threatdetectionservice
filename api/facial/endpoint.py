''' @Summary: API endpoint for accessing facial recognition services through MSFT Engine '''

from flask_restful import Resource, reqparse
from api import login_required
from api.sql.models import *  #import all of the models from models.py
from flask import send_file, request
import os, uuid, imghdr, time
from .MSFTFacialEngine import MSFTFacialEngine

class manageFacial(Resource):
    @login_required
    def get(self):
        print("MSFT Engine API Key %s", app.config['FACIAL_MSFT_API_KEY'])

class manageFacialSearch(Resource):
   # Get the images they are being searched for 
   def get(self,_customerID_,_userID_,_fileName_):
        try:
            return send_file("/home/mack/threatdetectionservice/api/facial/images/" + _customerID_ + "/search/" + _userID_ + "/" +_fileName_)
        except OSError as err:
            print("OS error: {0}".format(err))

   def post(self,_customerID_,_userID_):
        _customerID_ = "dpd"
        _userID_ = "dpd_user"
        baseSearchDir = "/home/mack/threatdetectionservice/api/facial/images/" + _customerID_ + "/search/"
        searchDir = "/home/mack/threatdetectionservice/api/facial/images/" + _customerID_ + "/search/" + _userID_
    
        # - Create a unique name and store the image under the customer/company ID and userid
        # Create the directory
        if not os.path.exists(searchDir):
            os.makedirs(searchDir)

        # Create a filename using UUID
        filename = uuid.uuid4().hex

        # Full Filename
        fullFilename = searchDir + "/" + filename


        # Save the image
        data = request.get_data()

        # Figure out the type of image
        imageType = imghdr.what(None,data)
        if (imageType != None):
            fullFilename = fullFilename + "." + imageType

        with open(fullFilename, 'wb') as f:
               f.write(data) 
               f.close()
        
        imageURL = self.getSearchImageURL(_customerID_.strip(),_userID_.strip(),filename.strip() + "." + imageType.strip())
        print(imageURL)
        
        if (isinstance(imageURL,str)):
            print("***This is a str")
         
        #time.sleep(30)
        # Start Search
        engine = MSFTFacialEngine()
        engine.setAPIKey("e0ace679238e4af9a6217f460a1378d5")
        found = engine.search("http",imageURL)

        jsonResult = {"searchImage":imageURL, "results":found}
        return jsonResult

    # - All images uploaded should be converted ot jpg, gif or bmp if not already in that format
    # - Kick off a search.  Which includes adding an entry in a table to keep track of searchs. The user should see
    #   all active and finished searchs.  Searchs are deleted when they close the search window
     
   def getSearchImageURL(self,customerID,userID,fileName):
        #url = app.config['EXTERNAL_URL'] + "/api/facial/search/" + customerID + "/" + userID + "/" + fileName 
        #url = "http://50.253.243.17:7777/api/facial/search/dpd/dpd_user/4040cdf442e44678a2f4c90e51ca6d8b.png"
        url = "http://50.253.243.17:7777/api/facial/search/dpd/dpd_user/4040cdf442e44678a2f4c90e51ca6d8b.png"
        url = "http://50.253.243.17:7777/api/facial/search/dpd/dpd_user/4040cdf442e44678a2f4c90e51ca6d8b.png"
        return url

class manageFacialRepo(Resource):
    def get(self,_customerID_,_fileName_):
        try:
            #imageBinary = open("/home/mack/threatdetectionservice/api/facial/images/" + _customerID_ + "/repo/" + _fileName_,'rb').read()
            return send_file("/home/mack/threatdetectionservice/api/facial/images/" + _customerID_ + "/repo/" + _fileName_)
        except OSError as err:
            print("OS error: {0}".format(err))
