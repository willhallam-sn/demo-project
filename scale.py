#!/bin/python3

import json
import subprocess
import sys

# initialize
incr=1
newReplicas=0

# parse args
serviceName=sys.argv[1]
upDown=sys.argv[2]

if (len(sys.argv)>3):
    incr=sys.argv[3]


# read config file

# cluster name from config file

# update Kubeconfig
updateKubeconfig=subprocess.run(["aws","--region","us-east-1","eks","update-kubeconfig","--name","hallam-1"])

# retrieve JSON for existing object
getResource=subprocess.run(["kubectl","get","-n","demo-project","-f",serviceName+".yaml","-o","json"],stdout=subprocess.PIPE,encoding='UTF-8')

serviceJson=json.loads(getResource.stdout)
if (upDown=="up"):
    newReplicas=serviceJson["spec"]["replicas"]+int(incr)
if (upDown=="down"):
    newReplicas=serviceJson["spec"]["replicas"]-int(incr)

if (newReplicas>0):
    kubeScale=subprocess.run(["kubectl","scale","-n","demo-project","--replicas",str(newReplicas),"-f",serviceName+".yaml"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='UTF-8')
    print (kubeScale.stdout)
    print (kubeScale.stderr)
