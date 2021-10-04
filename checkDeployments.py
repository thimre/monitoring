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
    url = baseUrl + "/apis/apps/v1/namespaces/" + ns + "/deployments"
    try:
        resp = requests.get(url, headers=headers, verify=cacert)
    except:
        print(f"Cannot connect to API at URL: {url}")
        sys.exit(2)
    return resp.json()


def getDepStateInNs(deps, ns):
    for dep in deps:
        name = dep.get("metadata").get("name")

        # Replicas is the number of desired replicas in .spec
        desired = dep.get("spec").get("replicas")

        if desired != 0:
            status = dep.get("status")

            # Replicas is the total number of pods targeted by this deployment config in .status
            replicas = status.get("replicas")

            # Total number of ready pods targeted by this deployment in .status
            readyReplicas = status.get("readyReplicas")

            if readyReplicas != desired:
                errors.append(["Deployment Not Ready. Namespace: " + ns + ", Name: " + name + ", Desired: " + str(desired) + ", Ready: " + str(readyReplicas)])

for oneNS in namespaces:
    response = makeRequest(oneNS)
    depsInOneNs = response.get("items")
    if depsInOneNs != None:
        getDepStateInNs(depsInOneNs, oneNS)


if len(errors) == 0:
    print("Ok")
    sys.exit(0)
else:
    print(errors)
    sys.exit(2)
