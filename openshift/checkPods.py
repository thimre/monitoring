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
    url = baseUrl + "/api/v1/namespaces/" + ns + "/pods"

    try:
        resp = requests.get(url, headers=headers, verify=cacert)
    except:
        print(f"Cannot connect to API at URL: {url}")
        sys.exit(2)
    return resp.json()


# Docs: https://docs.openshift.com/container-platform/3.11/rest_api/core/pod-core-v1.html

def getPodsStateInNs(pods, ns):
    for pod in pods:
        podReady = False

        status = pod.get("status").get("phase")
        name = pod.get("metadata").get("name")

        if status != "Succeeded":
            if status != "Running":
                errors.append(["Pod is " + status + ", Namespace: " + ns + ", Pod Name: " + name])

for oneNS in namespaces:
    response = makeRequest(oneNS)
    podsInOneNs = response.get("items")
    if podsInOneNs != None:
        getPodsStateInNs(podsInOneNs, oneNS)


if len(errors) == 0:
    print("Ok")
    sys.exit(0)
else:
    for err in errors:
        print(err)
    sys.exit(2)
