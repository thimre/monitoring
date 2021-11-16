#### Openshift (OKD) 3.11 monitoring scripts written in Python 3
---
The scripts communicate with the Openshift API using python's requests library. Their output is icinga / nagios compatible.

*Summary of the scripts:*
- __checkDeployments.py__ : Checks all deployments in the defined namespaces. It compares the total number of __ready pods__ targeted by a deployment, if it's not the same as the __desired__ number, exits with exit status 2 and outputs the name of the erroneous deployments. 
- __checkDeploymentConfigs.py__: Checks all deploymentconfig objects in the defined namespaces. It compares the total number of __ready pods__ targeted by a deploymentconfig, if it's not the same as the __desired__ number, exits with exit status 2 and outputs the name of the erroneous deploymentconfigs.
- __checkPods.py__: Checks all pods in the defined namespaces. Outputs the erroneous pods' name that are __not__ in __Running or Succeeded__ state and exits with 2.
- __checkReplicationControllers.py__: Checks all replication controllers in the defined namespaces. It compares the total number of __ready pods__ targeted by a replication controller, if it's not the same as the __desired__ number, exits with exit status 2 and outputs the name of the erroneous replication controllers.
- __checkDaemonSets.py__: Checks all daemonsets in the defined namespaces. It compares the __desiredNumberScheduled__ and __numberReady__ values in the daemonsets status.
*If there are no problems each script exits with exit status 0 and outputs OK.*

*Configuration:*

| variable | description | example |
| :--- | :--- | :--- |
| token64="" | The bearer token of the service account encoded in base64 | "abcde" |
| baseUrl="" | The url of the master node | "https://myOKDCluster.home:8443" | 
| cacert="" | The CA certificate of the cluster | "/etc/origin/master/ca.crt" |  
| namespaces=[] | The namespaces we want to monitor, the service account needs to have access to them | ["test1", "test2"] |  

*__In order to get the token you need to create a service account, and bind it to every namespace you want to monitor.__*

This will create a service account in the openshift-monitoring namespace, and bind the view clusterrole to it in the appropriate namespaces.  
- oc create sa nrpe-sa -n openshift-monitoring  
- oc policy add-role-to-user view system:serviceaccount:openshift-monitoring:nrpe-sa -n test1  
- oc policy add-role-to-user view system:serviceaccount:openshift-monitoring:nrpe-sa -n test2

To get the token in base64, first get the name of the secret (nrpe-sa-token-xxxxx) which stores the token:
- oc get sa nrpe-sa -n openshift-monitoring -o yaml
- oc get secret nrpe-sa-token-xxxxx -n openshift-monitoring -o yaml | grep "token:" | awk '{print $2}'  
*The output can be a value of token64 in the script.*  

---
[Openshift 3.11 REST API documentation](https://docs.openshift.com/container-platform/3.11/rest_api/)

