import requests, sys, base64

# v1.0

####
# b64 encoded token
#token64=""
#baseUrl=""
#cacert=""
####

token=base64.b64decode(token64.encode('ascii')).decode('utf-8')
headers = {"Authorization": "Bearer " + token}
errors = []

def makeRequest():
    url = baseUrl + "/api/v1/nodes"

    try:
        resp = requests.get(url, headers=headers, verify=cacert)
    except:
        print(f"Cannot connect to API at URL: {url}")
    return resp.json()


# Docs: https://docs.openshift.com/container-platform/3.11/rest_api/core/node-core-v1.html#node-core-v1

# The condition of these flags in status.conditions should be false, if it isn't, create an error
falseConditions = ["OutOfDisk", "MemoryPressure", "DiskPressure", "PIDPressure"]

response=makeRequest()
if response.get("items") != None:
  allNodes=response.get("items")
  for node in allNodes:
    nodeName=node.get("metadata").get("name")
    
    nodeConditions=node.get("status").get("conditions")
    for condition in nodeConditions:
      if condition.get("type") == "Ready":
        if condition.get("status") != "True":
          errors.append(nodeName + " is not ready. " + "Message: " + condition.get("message") + ", Reason: " + condition.get("reason"))
      for falseCondition in falseConditions:
        if condition.get("type") == falseCondition: 
          if condition.get("status") != "False":
            errors.append(nodeName + " " + condition.get("message") + ", Reason: " + condition.get("reason"))
            

if len(errors) == 0:
    print("Ok")
    sys.exit(0)
else:
    for err in errors:
        print(err)
    sys.exit(2)
