import requests, sys, base64

# v1.0

####
# b64 encoded token
token64=""
baseUrl=""
cacert=""
namespaces=[]
####

token=base64.b64decode(token64.encode('ascii')).decode('utf-8')
headers = {"Authorization": "Bearer " + token}
errors = []

def makeRequest(ns):
    url = baseUrl + "/api/v1/namespaces/" + ns + "/replicationcontrollers"
    try:
        resp = requests.get(url, headers=headers, verify=cacert)
    except:
        print(f"Cannot connect to API at URL: {url}")
        sys.exit(2)
    return resp.json()

# Docs: https://docs.openshift.com/container-platform/3.11/rest_api/core/replicationcontroller-core-v1.html

def getRCStateInNs(rcs, ns):
    for rc in rcs:
        rcReady = False
        name = rc.get("metadata").get("name")

        # Replicas is the number of desired replicas in .spec
        desired = rc.get("spec").get("replicas")

        if desired != 0:
            status = rc.get("status")

            # Replicas is the total number of pods targeted by this deployment config in .status
            replicas = status.get("replicas")

            # Total number of ready pods targeted by this deployment in .status
            readyReplicas = status.get("readyReplicas")


            #availableReplicas = status.get("availableReplicas")
            #updatedReplicas = status.get("updatedReplicas")
            #unavailableReplicas = status.get("unavailableReplicas")

            if readyReplicas == desired:
                rcReady = True
                #print([ns + " : " + name + " - Desired: " + str(desired) + ", Ready: " + str(readyReplicas)])
            else:
                #errors.append([ns + " : " + name + " - Replication Controller Not Ready. Desired: " + str(desired) + ", Ready: " + str(readyReplicas)])
                errors.append(["Replication Controller Not Ready. Namespace: " + ns + ", Name: " + name + ", Desired: " + str(desired) + ", Ready: " + str(readyReplicas)])


for oneNS in namespaces:
    response = makeRequest(oneNS)
    depsInOneNs = response.get("items")
    if depsInOneNs != None:
        getRCStateInNs(depsInOneNs, oneNS)


if len(errors) == 0:
    print("Ok")
    sys.exit(0)
else:
    print(errors)
    sys.exit(2)

