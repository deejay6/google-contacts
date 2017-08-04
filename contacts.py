import urllib2
import json
from client_secret import access_token
BASE_URL = "https://people.googleapis.com/v1/"
ACCESS_TOKEN = "Bearer  " + access_token
HOST = "people.googleapis.com"

content = ""


def retrieve_contacts():
    req = urllib2.Request(BASE_URL + 'people/me/connections?requestMask.includeField=person.names%2Cperson.phone_numbers')
    req.add_header('Host','people.googleapis.com')
    req.add_header('Authorization',ACCESS_TOKEN)
    resp = urllib2.urlopen(req)
    content = resp.read()
    d = json.loads(content)
    with open("retrieve.json", 'w') as outfile:
        json.dump(d,outfile)
    return d


def display_contacts():
    contacts = retrieve_contacts()
    for i in range(len(contacts['connections'])):
        print contacts['connections'][i]['names'][0]['displayName']
        print contacts['connections'][i]['phoneNumbers'][0]['canonicalForm']

# For deleting a contact first we need to retrieve all the contacts then comparing the results with the phone number that we want
# # to delete and finding the corresponding resource name. Deletion is done through resource name.


def delete_contacts():
    resource_name = None
    contacts = retrieve_contacts()
    phone = raw_input("Enter Phone Number : ")
    phone1 = "+91" + phone
    for i in range(len(contacts['connections'])):
      if contacts['connections'][i]['phoneNumbers'][0]['canonicalForm'] == phone1:
            resource_name = contacts['connections'][i]['resourceName']
            print resource_name
            break
    if resource_name:
        url = BASE_URL + resource_name + ':deleteContact'
        # url = 'https://people.googleapis.com/v1/people/c4045687748708784236:deleteContact'
        print url
        req = urllib2.Request(url)
        req.add_header('Host', HOST)
        req.add_header('Authorization',ACCESS_TOKEN)
        req.get_method = lambda: 'DELETE'  # creates the delete method
        resp = urllib2.urlopen(req)
        content = resp.read()
        d = json.loads(content)
        print d
    else:
        print "Number Not Found"


def add_contacts():
    name = raw_input("Enter Name: ")
    phone = raw_input("Enter Phone Number : ")
    phone1 = "+91" + phone
    payload = {
       "names": [
        {
         "givenName": name
        }
        ],
        "phoneNumbers": [
        {
         "canonicalForm": phone1,
         "value":phone
        }
        ]
      }
    payload = json.dumps(payload)
    print payload
    url = BASE_URL + "people:createContact"
    print url
    req = urllib2.Request(url)
    req.add_header('Host', HOST)
    req.add_header('Authorization', ACCESS_TOKEN)
    req.add_data(payload)
    resp = urllib2.urlopen(req)
    content = resp.read()
    d = json.loads(content)
    print d

# For updating a contact we need to have eTag and resource name of person


def update_contacts():
    resource_name = None
    e_tag = None
    phone = raw_input("Enter Phone Number To be Updated : ")
    phone1 = "+91" + phone
    name = raw_input("Enter Name:  ")
    phone2 = raw_input("Enter Updated Phone Number: ")
    contacts = retrieve_contacts()
    for i in range(len(contacts['connections'])):
        if contacts['connections'][i]['phoneNumbers'][0]['canonicalForm'] == phone1:
            resource_name = contacts['connections'][i]['resourceName']
            e_tag = contacts['connections'][i]['etag']
            print e_tag
            print resource_name
            break
    if resource_name:
        payload = \
                {
                 "etag": e_tag,
                 "names": [
                  {
                   "givenName": name
                  }
                 ],
                 "phoneNumbers": [
                  {
                   "value": phone2,
                   "canonicalForm": '+91'+phone2
                  }
                 ]
                }
        print payload
        payload = json.dumps(payload)
        with open("add.txt",'w') as outfile:
           outfile.write(payload)
        url = BASE_URL + resource_name + ":updateContact?updatePersonFields=phoneNumbers%2Cnames&fields=names%2CphoneNumbers"
        print url
        req = urllib2.Request(url)
        req.add_data(payload)
        req.add_header('Host', HOST)
        req.add_header('Authorization', ACCESS_TOKEN)
        req.get_method = lambda: 'PATCH'  # creates the PATCH method similar to PUT
        resp = urllib2.urlopen(req)
        content = resp.read()
        d = json.loads(content)
        print d

# display_contacts()
# delete_contacts()
# add_contacts()
# update_contacts()