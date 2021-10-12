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
    url = baseUrl + "/apis/apps/v1/namespaces/" + ns + "/daemonsets"
    try:
        resp = requests.get(url, headers=headers, verify=cacert)
    except Exception as e:
        print(f"Cannot connect to API at URL: {url}")
        print(e)
        sys.exit(2)
    return resp.json()

# Docs: https://docs.openshift.com/container-platform/3.11/rest_api/apps/daemonset-apps-v1.html#daemonset-apps-v1

def getDsStateInNs(dss, ns):
    for ds in dss:
        name = ds.get("metadata").get("name")
        status = ds.get("status")
        desiredNumberScheduled = status.get("desiredNumberScheduled")

        if desiredNumberScheduled != 0:

            # numberReady: The number of nodes that should be running the daemon pod and have one or more of the daemon pod running and ready.
            numberReady = status.get("numberReady")

            if numberReady == desiredNumberScheduled:
                print([ns + " : " + name + " - Desired: " + str(desiredNumberScheduled) + ", Ready: " + str(readyReplicas)])
            else:
                errors.append(["DaemonSet Not Ready. Namespace: " + ns + ", Name: " + name + ", Desired: " + str(desiredNumberScheduled) + ", Ready: " + str(numberReady)])


for oneNS in namespaces:
    response = makeRequest(oneNS)
    dsInOneNs = response.get("items")
    if dsInOneNs != None:
        getDsStateInNs(dsInOneNs, oneNS)


if len(errors) == 0:
    print("Ok")
    sys.exit(0)
else:
    print(errors)
    sys.exit(2)
