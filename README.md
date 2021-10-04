#### Openshift 3.11, OKD 3.11 monitoring scripts written in Python 3.

*Configuration:*

| token64="" | # The bearer token of the service account encoded in base64 |  
|:---|:---|
baseUrl=""  # The url of the master node, ex: "https://myOKDCluster.home:8443"  
cacert="" # The CA certificate of the cluster, ex: "/etc/origin/master/ca.crt"  
namespaces=[]  # The namespaces we want to monitor, the service account needs to have access to them. Ex: ["test1", "test2"]  
