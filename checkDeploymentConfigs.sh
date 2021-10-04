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
    url = baseUrl + "/apis/apps.openshift.io/v1/namespaces/" + ns + "/deploymentconfigs"
    try:
        resp = requests.get(url, headers=headers, verify=cacert)
    except Exception as e:
        print(f"Cannot connect to API at URL: {url}")
        print(e)
        sys.exit(2)
    return resp.json()

# Docs: https://docs.openshift.com/container-platform/3.11/rest_api/apps_openshift_io/deploymentconfig-apps-openshift-io-v1.html

def getDepcfgsStateInNs(deps, ns):
    for dep in deps:
        depReady = False
        name = dep.get("metadata").get("name")

        # Replicas is the number of desired replicas in .spec
        desired = dep.get("spec").get("replicas")

        if desired != 0:
            status = dep.get("status")

            # Replicas is the total number of pods targeted by this deployment config in .status
            replicas = status.get("replicas")

            # Total number of ready pods targeted by this deployment in .status
            readyReplicas = status.get("readyReplicas")


            #availableReplicas = status.get("availableReplicas")
            #updatedReplicas = status.get("updatedReplicas")
            #unavailableReplicas = status.get("unavailableReplicas")

            if readyReplicas == desired:
                depReady = True
                #print([ns + " : " + name + " - Desired: " + str(desired) + ", Ready: " + str(readyReplicas)])
            else:
                #errors.append([ns + " : " + name + " - Deployment Not Ready. Desired: " + str(desired) + ", Ready: " + str(readyReplicas)])
                errors.append(["Deployment Not Ready. Namespace: " + ns + ", Name: " + name + ", Desired: " + str(desired) + ", Ready: " + str(readyReplicas)])


for oneNS in namespaces:
    response = makeRequest(oneNS)
    depsInOneNs = response.get("items")
    if depsInOneNs != None:
        getDepcfgsStateInNs(depsInOneNs, oneNS)


if len(errors) == 0:
    print("Ok")
    sys.exit(0)
else:
    print(errors)
    sys.exit(2)
