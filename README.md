#### Openshift 3.11, OKD 3.11 monitoring scripts written in Python 3.

*Configuration:*

| variable | description | example |
| :--- | :--- | :--- |
| token64="" | The bearer token of the service account encoded in base64 | |
| baseUrl="" | The url of the master node | "https://myOKDCluster.home:8443" | 
| cacert="" | The CA certificate of the cluster | "/etc/origin/master/ca.crt" |  
| namespaces=[] | The namespaces we want to monitor, the service account needs to have access to them | ["test1", "test2"] |  

In order to get the token you need to create a service account, and bind it to every namespace you want to monitor.

This will create a service account in the openshift-monitoring namespace, and bind the view clusterrole to it in the appropriate namespaces.  
oc create sa nrpe-sa -n openshift-monitoring  
oc policy add-role-to-user view system:serviceaccount:openshift-monitoring:nrpe-sa -n test1  
oc policy add-role-to-user view system:serviceaccount:openshift-monitoring:nrpe-sa -n test2  
