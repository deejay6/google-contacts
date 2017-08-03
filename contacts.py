import urllib2
import json
BASE_URL = "https://people.googleapis.com/v1/people/"
content = ""


def retrieve():
  req = urllib2.Request(BASE_URL + 'me/connections?requestMask.includeField=person.names%2Cperson.phone_numbers')
  req.add_header('Host','people.googleapis.com')
  req.add_header('Authorization','access_token')
  req.add_header('Content-Type','application/json')
  resp = urllib2.urlopen(req)
  content = resp.read()
  d = json.loads(content)
  print len(d['connections'])
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
  phone = int(raw_input("Enter Phone Number with canonical form (+91) : "))
  for i in range(len(contacts['connections'])):
    if contacts['connections'][i]['phoneNumbers'][0]['canonicalForm']:
      resource_name = contacts['connections'][i]['resourceName']
      print str(resource_name)
      # resource_name.encode('utf-8')
      print type(resource_name)
      break
  if resource_name:
    req = urllib2.Request(BASE_URL + '%s:deleteContact') % (resource_name)
    req.add_header('Host', 'people.googleapis.com')
    req.add_header('Authorization',
                   'access_token')
    req.add_header('Content-Type', 'application/json')
    resp = urllib2.urlopen(req)
    content = resp.read()
    d = json.loads(content)
    print d
  else:
    print "Number Not Found"

delete()