# pg-aws-python
Very minimalistic and simple python scripts Bourne from Shell scripts. Automating my day to day with simple scripts.

###### This README is more like a note-to-self-style-documentation.

### All the scripts assume that you are logged into aws and credentials are available as env vars.


1. ```ecs-deploy.py```

 This is a very basic python script which doesn't cater for boiling the entire aws ecs ocean. Then what does it do ?
 So, lets assume that you have a service name ```my-banana-service``` running on AWS's ecs cluster named ```my-smoothie-cluster```.
 And you want to deploy a new docker image versioned ```my-vegan-version``` for that particular service. Either you would do it via AWS Console or via
 aws-cli (whole bunch of steps). This script essentially abstracts the need for you knowing any of the aws shenanigans
 to do the ecs shenanigans. In order to do a deploy ... all you need to do is:
  1. Log in to your aws-cli (or use your keys)
  1. Run the script.

  ### How do I run this script?
  In order to run the script please make sure you have python3, pip3 and boto3 installed.
  
  Run ```python3 ./src/ecs-deploy.py -h ```
  
  The above command prints help for the script listing out the params that could be passed. In our instance we would  run the following:
  
  ```python3 ./src/ecs-deploy.py -c "my-smoothie-cluster" -s "my-banana-service" -i "my-vegan-version" ```
  
  This would register a new task definition and update the service with this new task definition.