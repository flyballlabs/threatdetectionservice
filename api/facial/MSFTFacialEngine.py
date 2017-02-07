from .FacialEngine import FacialEngine
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json, requests
import os,sys
sys.path.append('/home/mack/threatdetectionservice/')
from api import *
from  api.sql.models import *


class MSFTFacialEngine(FacialEngine):
    name = "MSFT Facial Engine"
    hostname = "westus.api.cognitive.microsoft.com"
    endpoint  = "/face"
    apiVersion = "v1.0"
    customerID = "dpd"
    baseImageDir = "/home/mack/threatdetectionservice/api/facial/images"
    siteImageURL = "http://50.253.243.17:7777/api/facial/images" 

    # Load the image repository (from scratch each time) into the engine (aka API service)
    # type - protocol to use (eg. ftp, http, file, etc)
    # uri - the location to the data. If file, then the uri would be relative path to the files
    def loadRepo(self,type, uri):
        if type == "file":
           #Define the URL that we need to access
            opURL = self.endpoint + "/" + self.apiVersion + "/facelists" + "/" + self.customerID
            #_body= "{'name': {0}}" 
            _body = {'name': self.customerID}
           #Create facelist based on the customerID
            print("Trying to create a new facelist: opURL:",opURL)
            r = self.invoke(self.hostname, opURL,"PUT",json.dumps(_body))
            if (r['code'] !=  200 ):
                print("Deleting the {0} facelist".format(self.customerID))
                # If already exists, delete the existing facelist
                r = self.invoke(self.hostname, opURL,"DELETE",json.dumps(_body))
                if (r['code']  == 200 ):
                    # Recreate the facelist from scratch
                    r = self.invoke(self.hostname, opURL,"PUT",json.dumps(_body))
                    if (r['code'] == 200):
                       print("New facelist {0} was created".format(self.customerID))
            else:
                print("New facelist {0} was created".format(self.customerID)) 
           #Make sure the images are available via http 
           
           #Add the images to the facelist via the MSFT API
            self.add_faces(opURL)
        return True

    def add_faces(self,opURL):
        directory = self.baseImageDir + "/" + self.customerID + "/repo"
        print(directory)
        images = []
        persistIDtoImage = {}
        JSONImageList ="{"

        opURL = opURL + "/" + "persistedFaces"
        
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".gif"): 
               imageURL = self.siteImageURL + "/" + self.customerID + "/repo/" + filename 
               print(imageURL)
               jsonBody = "{" +  "\"url\":" + "\"" + imageURL + "\"" + "}"
               print(opURL)
               r = self.invoke(self.hostname, opURL,"POST",jsonBody)
               if (r['code'] == 200):
                   print(r['response'])
                   response = json.loads(r['response']) 
                   # Maintain a mapping between the persistedFaceId returned by MSFT and the actual image URL
                   persistIDtoImage[response['persistedFaceId']] = imageURL
                   #Store the data in the database
                   query = facial_image_data(company_id=self.customerID,image_name=filename,image_http_url=imageURL,engine_type="MSFT",face_id=response['persistedFaceId'],facelist_id=self.customerID)
                   curr_session = db.session
                   try:
                       curr_session.add(query) #add prepared statement
                       curr_session.commit() #commit changes
                   except:
                       print(e);
                       curr_session.rollback()
                       curr_session.flush()
            else:
                continue
        
        print(persistIDtoImage)
        return persistIDtoImage

    def search(self,type,uri):
        #uri = "http://50.253.243.17:7777/api/facial/search/dpd/dpd_user/1280_jeremy_meeks_hot_mugshot_guy.jpg"       
        #uri = "http://www.etonline.com/news/2016/06/24246818/1280_jeremy_meeks_hot_mugshot_guy.jpg"
        #uri = "http://edge.dopensource.com:7777/api/facial/search/dpd/dpd_user/6af91cea433d4cf7a55a3b06cd50c312.png"
        #uri = "http://50.253.243.17:7777/api/facial/search/dpd/dpd_user/4040cdf442e44678a2f4c90e51ca6d8b.png"
        found = []
        # Call Facial Detect
        opURL = self.endpoint + "/" + self.apiVersion + "/detect"
        jsonBody = {
                     'url': uri
                   }
        r = self.invoke(self.hostname, opURL,"POST",jsonBody)
        if (r['code'] == 200):
                   print(r['response'])
                   response = json.loads(r['response']) 
                   for element in response:
                       if (element['faceId'] != None):
                           queryFaceID = element['faceId']
                           print(queryFaceID)
        else:
            return None
       # Look for facial match
      
        opURL = self.endpoint + "/" + self.apiVersion + "/findsimilars"
        jsonBody = { 
                     'faceId':queryFaceID,
                     'faceListId':self.customerID
          }
        print(jsonBody)
        r = self.invoke(self.hostname, opURL,"POST",jsonBody)
        if (r['code'] == 200):
                   print(r['response'])
                   response = json.loads(r['response'])
                   for element in response:
                      if (element['persistedFaceId'] != None):
                         record = {}
                         record['image'] = self.getImageURL(element['persistedFaceId'])
                         record['confidence'] = element['confidence']
                         found.append(record) 
        return found 

    def getImageURL(self,persistedFaceId):
        try:
                x = facial_image_data.query.filter_by(face_id=persistedFaceId).first()
                if x != None:
                    return x.image_http_url
        except Exception as e:
            return {'error': str(e)}

    def invoke(self,hostname,url,action="POST",body=None):
            #print("In Invoke:" + body) 
            result = {}
            _headers= { 
                    
                'Ocp-Apim-Subscription-Key' : self.getAPIKey(),
                'Content-Type' : 'application/json',
            }
   
            params = urllib.parse.urlencode({
            })

            try:
            
                fullURL = "https://" + hostname + url
                print(fullURL)
                response = requests.request(action,fullURL,json=body,headers=_headers)
            #    conn = http.client.HTTPSConnection(self.hostname)
            #    if (body == None):
            #        conn.request(action, url,headers= _headers)
            #    else:
            #        conn.request(action, url,body,_headers)
            #        print("Finished request with body")
            #    response = conn.getresponse()
            #    #data = str(response.read())
            #    data = response.read().decode('utf8')
            #    conn.close()
            except Exception as e:
                  print("[Errno {0}] {1}".format(e.errno, e.strerror)) 
                  result['code'] = 404
                  result['response'] = data
                  return result
            if response.status_code in (200, 202):
                  result['code'] = response.status_code
                  result['response'] = response.text
                  print(response.text)
                  return result 
            else:
                  result['code'] = response.status_code
                  result['response'] = response.text  
                  print(response.text)
                  return result 


            #if data.find("error") != -1:
            #    print(data)
            #    result['code'] = 404
            #    result['response'] = data
            #    return result
            #else:
            #    result['code'] = 200
            #    result['response'] = data
            #    return result

if __name__ == "__main__":
    db.create_all()
    app = MSFTFacialEngine()
    app.setAPIKey("e0ace679238e4af9a6217f460a1378d5")
    print(app.getName())
    print("API Key:" + app.getAPIKey())
    #app.createJSONImageList()
    #app.loadRepo("file", "facialimages/dpd/repo");
    f = app.search("http","http://50.253.243.17:7777/api/facial/images/dpd/repo/williamaikin1.jpg")
    print(f)
    #image = app.getImageURL('494a2a16-353a-442d-ba07-5ac70d8a1dcd')
    #print(image)
