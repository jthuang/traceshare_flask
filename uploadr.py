#!/usr/bin/env python

import sys
import hashlib
import mimetools
import mimetypes
import os
import urllib
import urllib2
import webbrowser
import json
from xml.dom.minidom import parse
import base64
import tempfile

FLICKR = {
        "title"                 : "",
        "description"           : "",
        "tags"                  : "trace-share",
        "is_public"             : "1",
        "is_friend"             : "0",
        "is_family"             : "0",
        "api_key"               : "06378d89754dd629d0a11295a33e246b",
        "secret"                : "adc096544fb20f32"
        }
TOKEN_PATH = ".flickrToken"




class APIConstants:
    """ APIConstants class
    """

    base = "https://api.flickr.com/services/"
    rest   = base + "rest/"
    auth   = base + "auth/"
    upload = base + "upload/"
    replace = base + "replace/"

    def __init__( self ):
       """ Constructor
       """
       pass

api = APIConstants()

class Uploadr:
    """ Uploadr class
    """

    token = None
    perms = ""

    def __init__( self ):
        """ Constructor
        """
        self.token = self.getCachedToken()


    def signCall( self, data):
        """
        Signs args via md5 per http://www.flickr.com/services/api/auth.spec.html (Section 8)
        """
        keys = data.keys()
        keys.sort()
        foo = ""
        for a in keys:
            foo += (a + data[a])

        f = FLICKR[ "secret" ] + "api_key" + FLICKR[ "api_key" ] + foo

        return hashlib.md5( f ).hexdigest()

    def urlGen( self , base,data, sig, need_sig=True):
        """ urlGen
        """
        data['api_key'] = FLICKR[ "api_key" ]
        if need_sig:
           data['api_sig'] = sig
        encoded_url = base + "?" + urllib.urlencode( data )
        return encoded_url


    def authenticate( self ):
        """ Authenticate user so we can upload files
        """

        print("Getting new token")
        self.getFrob()
        self.getAuthKey()
        self.getToken()
        self.cacheToken()

    def getFrob( self ):
        """
        flickr.auth.getFrob

        Returns a frob to be used during authentication. This method call must be
        signed.

        This method does not require authentication.
        Arguments

        "api_key" (Required)
        Your API application key. See here for more details.
        """

        d = {
            "method"          : "flickr.auth.getFrob",
            "format"          : "json",
            "nojsoncallback"    : "1"
            }
        sig = self.signCall( d )
        url = self.urlGen( api.rest, d, sig )
        try:
            response = self.getResponse( url )
            if ( self.isGood( response ) ):
                FLICKR[ "frob" ] = str(response["frob"]["_content"])
            else:
                self.reportError( response )
        except:
            print("Error: cannot get frob:" + str( sys.exc_info() ))

    def getAuthKey( self ):
        """
        Checks to see if the user has authenticated this application
        """
        d =  {
            "frob"            : FLICKR[ "frob" ],
            "perms"           : "delete"
            }
        sig = self.signCall( d )
        url = self.urlGen( api.auth, d, sig )
        ans = ""
        try:
            webbrowser.open( url )
            print("Copy-paste following URL into a web browser and follow instructions:")
            print(url)
            ans = raw_input("Have you authenticated this application? (Y/N): ")
        except:
            print(str(sys.exc_info()))
        if ( ans.lower() == "n" ):
            print("You need to allow this program to access your Flickr site.")
            print("Copy-paste following URL into a web browser and follow instructions:")
            print(url)
            print("After you have allowed access restart uploadr.py")
            sys.exit()

    def getToken( self ):
        """
        http://www.flickr.com/services/api/flickr.auth.getToken.html

        flickr.auth.getToken

        Returns the auth token for the given frob, if one has been attached. This method call must be signed.
        Authentication

        This method does not require authentication.
        Arguments

        NTC: We need to store the token in a file so we can get it and then check it insted of
        getting a new on all the time.

        "api_key" (Required)
           Your API application key. See here for more details.
        frob (Required)
           The frob to check.
        """

        d = {
            "method"          : "flickr.auth.getToken",
            "frob"            : str(FLICKR[ "frob" ]),
            "format"          : "json",
            "nojsoncallback"    : "1"
        }
        sig = self.signCall( d )
        url = self.urlGen( api.rest, d, sig )
        try:
            res = self.getResponse( url )
            if ( self.isGood( res ) ):
                self.token = str(res['auth']['token']['_content'])
                self.perms = str(res['auth']['perms']['_content'])
                self.cacheToken()
            else :
                self.reportError( res )
        except:
            print(str(sys.exc_info()))


    def getCachedToken( self ):
        """
        Attempts to get the flickr token from disk.
       """
        if ( os.path.exists( TOKEN_PATH )):
            return open( TOKEN_PATH ).read()
        else :
            return None


    def cacheToken( self ):
        """ cacheToken
        """

        try:
            open( TOKEN_PATH , "w").write( str(self.token) )
        except:
            print("Issue writing token to local cache ", str(sys.exc_info()))


    def checkToken( self ):
        """
        flickr.auth.checkToken

        Returns the credentials attached to an authentication token.
        Authentication

        This method does not require authentication.
        Arguments

        "api_key" (Required)
            Your API application key. See here for more details.
        auth_token (Required)
            The authentication token to check.
        """

        if ( self.token == None ):
            return False
        else :
            d = {
                "auth_token"      :  str(self.token) ,
                "method"          :  "flickr.auth.checkToken",
                "format"          : "json",
                "nojsoncallback"  : "1"
            }
            sig = self.signCall( d )

            url = self.urlGen( api.rest, d, sig )
            try:
                res = self.getResponse( url )
                if ( self.isGood( res ) ):
                    self.token = res['auth']['token']['_content']
                    self.perms = res['auth']['perms']['_content']
                    return True
                else :
                    self.reportError( res )
            except:
                print(str(sys.exc_info()))
            return False


    def uploadFile( self, file ):
        """ uploadFile
        """

        success = False
        photoid = ""
        print("Uploading " + file + "...")
        try:
           photo = ('photo', file, open(file,'rb').read())

           d = {
                 "auth_token"    : str(self.token),
                 "perms"         : str(self.perms),
                 "title"         : str( FLICKR["title"] ),
                 "description"   : str( FLICKR["description"] ),
                 "tags"          : str( FLICKR["tags"] ),
                 "is_public"     : str( FLICKR["is_public"] ),
                 "is_friend"     : str( FLICKR["is_friend"] ),
                 "is_family"     : str( FLICKR["is_family"] )
           }
           
           sig = self.signCall( d )
           d[ "api_sig" ] = sig
           d[ "api_key" ] = FLICKR[ "api_key" ]
           
           url = self.build_request(api.upload, d, (photo,))
           res = parse(urllib2.urlopen( url ))
           if ( not res == "" and res.documentElement.attributes['stat'].value == "ok" ):
              print("Successfully uploaded the file: " + file)
              photoid_tag = res.getElementsByTagName('photoid')[0].toxml()
              photoid = photoid_tag.replace('<photoid>','').replace('</photoid>','')
              print "Photo ID:", photoid
              success = True
           else :
              print("A problem occurred while attempting to upload the file: " + file)
              try:
                 print("Error: " + str( res.toxml() ))
              except:
                 print("Error: " + str( res.toxml() ))
        except:
           print(str(sys.exc_info()))
        return success, photoid


    def getPhotoURL(self, photoid):
       photo_url = ""

       d = {
             "method"            : "flickr.photos.getSizes",
             "photo_id"          : photoid,
             "auth_token"        :  str(self.token) ,
             "format"            : "json",
             "nojsoncallback"    : "1"
           }

       sig= self.signCall(d)
       url = self.urlGen(api.rest, d, sig)
       print url
       try:
          response = self.getResponse( url )
          if ( self.isGood( response ) ):
             for photo_link in response["sizes"]["size"]:
                if photo_link["label"] == "Original":
                   photo_url = photo_link["source"]
                   break
          else:
             self.reportError( response )
       except:
          print("Error: cannot get photo URL:" + str( sys.exc_info() ))

       return photo_url


    def getPhotoGeoInfo(self, photoid):
       geo_lat = ""
       geo_long = ""
       geo_accuracy = ""
       d = {
             "method"            : "flickr.photos.geo.getLocation",
             "photo_id"          : photoid,
             "auth_token"        : str(self.token) ,
             "format"            : "json",
             "nojsoncallback"    : "1"
           }

       sig= self.signCall(d)
       url = self.urlGen(api.rest, d, sig)
       print url
       try:
          response = self.getResponse( url )
          if ( self.isGood( response ) ):
             geo_lat = response["photo"]["location"]["latitude"]
             geo_long = response["photo"]["location"]["longitude"]
             geo_accuracy = response["photo"]["location"]["accuracy"]
          else:
             self.reportError( response )
       except:
          print("Error: cannot get photo URL:" + str( sys.exc_info() ))

       return (geo_lat, geo_long, geo_accuracy)

    def getPhotoPlace(self, lat, lon, accuracy):
       geo_place = ""
       d = {
             "method"            : "flickr.places.findByLatLon",
             "lat"               : str(lat),
             "lon"               : str(lon),
             "accuracy"          : str(accuracy),
             "format"            : "json",
             "nojsoncallback"    : "1"
           }

       sig= self.signCall(d)
       url = self.urlGen(api.rest, d, sig, False)
       print url
       try:
          response = self.getResponse( url )
          if ( self.isGood( response ) ):
             geo_place = response["places"]["place"][0]["woe_name"]
          else:
             self.reportError( response )
       except:
          print("Error: cannot get photo URL:" + str( sys.exc_info() ))

       return geo_place



    def build_request(self, theurl, fields, files, txheaders=None):
        """
        build_request/encode_multipart_formdata code is from www.voidspace.org.uk/atlantibots/pythonutils.html

        Given the fields to set and the files to encode it returns a fully formed urllib2.Request object.
        You can optionally pass in additional headers to encode into the opject. (Content-type and Content-length will be overridden if they are set).
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.
        """

        content_type, body = self.encode_multipart_formdata(fields, files)
        if not txheaders: txheaders = {}
        txheaders['Content-type'] = content_type
        txheaders['Content-length'] = str(len(body))

        return urllib2.Request(theurl, body, txheaders)

    def encode_multipart_formdata(self,fields, files, BOUNDARY = '-----'+mimetools.choose_boundary()+'-----'):
        """ Encodes fields and files for uploading.
        fields is a sequence of (name, value) elements for regular form fields - or a dictionary.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files.
        Return (content_type, body) ready for urllib2.Request instance
        You can optionally pass in a boundary string to use or we'll let mimetools provide one.
        """

        CRLF = '\r\n'
        L = []
        if isinstance(fields, dict):
            fields = fields.items()
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            filetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % filetype)
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY        # what if no files are encoded
        return content_type, body

    def isGood( self, res ):
        """ isGood
        """

        if ( not res == "" and res['stat'] == "ok" ):
            return True
        else :
            return False

    def reportError( self, res ):
        """ reportError
        """

        try:
            print("Error: " + str( res['code'] + " " + res['message'] ))
        except:
            print("Error: " + str( res ))

    def getResponse( self, url ):
        """
        Send the url and get a response.  Let errors float up
        """

        try:
            res = urllib2.urlopen( url ).read()
        except urllib2.HTTPError, e:
            print(e.code)
        except urllib2.URLError, e:
            print(e.args)
        return json.loads(res)

def FlickrUpload(in_data):
    photo_info = {}

    flick = Uploadr()
    if FLICKR["api_key"] == "" or FLICKR["secret"] == "":
        print("Please enter an API key and secret in the script file (see README).")
        sys.exit()
    if ( not flick.checkToken() ):
        flick.authenticate()

    # Decode and save Base64 file
    out_data = base64.b64decode(in_data)
    (fd, fname) = tempfile.mkstemp(dir="")
    with os.fdopen(fd, 'w') as out_file:
       out_file.write(out_data)
    out_file.closed
    
    # upload a photo
    (result, photo_info['id']) = flick.uploadFile(fname)
    print result, photo_info['id']
    # after uploaded, remove the temp file
    os.remove(fname)

    # get photo URL
    photo_info['url'] = flick.getPhotoURL(photo_info['id'])
    print photo_info['url']

    # get photo geo info
    (photo_info['lat'], photo_info['long'], photo_info['accuracy']) = flick.getPhotoGeoInfo(photo_info['id'])
    print photo_info['lat'], photo_info['long'], photo_info['accuracy']

    # get photo place
    if photo_info['lat'] != "" and photo_info['long'] != "" and photo_info['accuracy'] != "":
       photo_info['place'] = flick.getPhotoPlace(photo_info['lat'], photo_info['long'], photo_info['accuracy'])
    else:
       photo_info['place'] = ""
    print photo_info['place']

    return photo_info


if __name__ == "__main__":
   if len(sys.argv) != 2:
      print "please enter the 'file name'."
   else:
      in_fname = sys.argv[1]
      
      with open(in_fname, 'r') as in_file:
         in_data = in_file.read()
      in_file.closed

      photo_info = FlickrUpload(in_data)
      print photo_info

