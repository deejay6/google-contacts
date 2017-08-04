import urllib2
import json
BASE_URL = "https://people.googleapis.com/v1/"
content = ""


def retrieve():
  req = urllib2.Request(BASE_URL + 'people/me/connections?requestMask.includeField=person.names%2Cperson.phone_numbers')
  req.add_header('Host','people.googleapis.com')
  req.add_header('Authorization',
                 'Bearer ya29.GlydBDLB1pCQyKaeRyratehN9WuyCokphL77RIMIiGVsvMdyeG6uZZzAJKjDe5BHFlWFOnFESOEzjY1zSG4FMEfZ2sOqLzx855WsIZSLu-8o8P2xyd11SzOOYhdbng')
  req.add_header('Content-Type','application/json')
  req.add_header('Method','Post')
  resp = urllib2.urlopen(req)
  content = resp.read()
  d = json.loads(content)
  print len(d['connections'])
  print d
  with open('data1.json','w') as outfile:
    json.dumps(d,outfile)
  return d


def display_contacts():
  contacts = retrieve()
  for i in range(len(contacts['connections'])):
    print contacts['connections'][i]['names'][0]['displayName']
    print contacts['connections'][i]['phoneNumbers'][0]['canonicalForm']

# For deleting a contact first we need to retrieve all the contacts then comparing the results with the phone number that we want
# # to delete and finding the corresponding resource name. Deletion is done through resource name.


def delete():
  resource_name = None
  contacts = retrieve()
  phone = raw_input("Enter Phone Number with canonical form (+91) : ")
  for i in range(len(contacts['connections'])):
    if contacts['connections'][i]['phoneNumbers'][0]['canonicalForm'] == phone:
      resource_name = contacts['connections'][i]['resourceName']
      e_tag = contacts['connections'][i]['etag']
      print e_tag
      print resource_name
      break
  if resource_name:
    url = BASE_URL + resource_name + ':deleteContact'
    url = 'https://people.googleapis.com/v1/people/c2747534632976151208:deleteContact'
    print url
    req = urllib2.Request(url)
    req.add_header('Host', 'people.googleapis.com')
    print req
    req.add_header('Authorization','ya29.GludBM5ja4022quS5lS72fkIolxYFAYZ17tccUGXiR0yk_EHyQ2f75CQdiO_taR__5zlQ37erUjpft3DRjkj39c4dc8rEBG3ZlsFmibudSLOSeRtNV14WSVgcTCU')
    print req
    req.add_header('Content-Type', 'application/json')
    print req
    resp = urllib2.urlopen(req)
    print "sucess"
    content = resp.read()
    d = json.loads(content)
    print d
  else:
    print "Number Not Found"


def add():
  name = raw_input("Enter Name: ")
  phone = raw_input("Enter Phone Number with canonical form (+91) : ")
  payload = {
   "names": [
    {
     "givenName": name
    }
    ],
    "phoneNumbers": [
    {
     "canonicalForm": phone
    }
    ]
  }
  print type(payload)
  payload = json.dumps(payload)
  print payload
  url = 'https://people.googleapis.com/v1/people:createContact'
  print url
  req = urllib2.Request(url)
  req.add_header('Host','people.googleapis.com')
  req.add_header('Authorization','Bearer ya29.GludBD77T97ClDpC35scJDwbj7px4kqtOcTQQhyAecyy9d1JNxSwJYU9X5GBoCPl782sGeLmbruh6o4dTR_G81aWPhrVIv2QLUFOvAuX4S-Hzhl2QfDiT6m-RvHA')
  req.add_header('Content-Type','application/json')
  req.add_data(payload)
  resp = urllib2.urlopen(req)
  content = resp.read()
  d = json.loads(content)
  print d

# For updating a contact we need to have eTag and resource name of person


def update():
  resource_name = None
  e_tag = None
  contacts = retrieve()
  phone = raw_input("Enter Phone Number To be Updated with canonical form (+91) : ")
  name = raw_input("Eter Name:  ")
  phone1 = raw_input("Enter Updated Phone Number: ")
  for i in range(len(contacts['connections'])):
    if contacts['connections'][i]['phoneNumbers'][0]['canonicalForm'] == phone:
      resource_name = contacts['connections'][i]['resourceName']
      e_tag = contacts['connections'][i]['etag']
      print e_tag
      print resource_name
      break
  payload = \
    {
     "etag": "%EgMBAgsaDQABAgMEBQYHCAkKCwwiDG8rNGZLMWtnbk5JPQ==",
     "names": [
      {
       "givenName": name
      }
     ],
     "phoneNumbers": [
      {
       "value": phone1,
       "canonicalForm": '+91'+phone1
      }
     ]
    }
  print payload
  payload = json.dumps(payload)
  url = BASE_URL + resource_name + ':updateContact?updatePersonFields=phoneNumbers%2Cnames&fields=names%2CphoneNumbers'
  print url
  req = urllib2.Request(url)
  req.add_header('Host', 'people.googleapis.com')
  req.add_header('Authorization',
                 'Bearer ya29.GlydBDLB1pCQyKaeRyratehN9WuyCokphL77RIMIiGVsvMdyeG6uZZzAJKjDe5BHFlWFOnFESOEzjY1zSG4FMEfZ2sOqLzx855WsIZSLu-8o8P2xyd11SzOOYhdbng')
  req.add_header('Content-Type', 'application/json')
  req.add_header('Method', 'Post')
  req.add_data(payload)
  resp = urllib2.urlopen(req)
  content = resp.read()
  d = json.loads(content)
  print d



update()