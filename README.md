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
     
      1. Log in to aws if you have sso enabled for cli access, or if you use something like credulous make sure you have appropriate shell vars.
      1. Run the script.

      *How do I run this script?*
      
      Run ```python3 ./src/ecs-deploy.py -h ```
      
      The above command prints help for the script listing out the params that could be passed. In our instance we would  run the following:
      
      ```python3 ./src/ecs-deploy.py -c "my-smoothie-cluster" -s "my-banana-service" -i "my-vegan-version" ```
      
      This would register a new task definition and update the service with this new task definition.

1. ```kms-decrypt.py```

     KMS is one of the very powerful and easy to use service, where AWS takes the ownership of keys and the customers use them to encrypt there secrets. 
     More often then not there is a need to verify or check, if the KMS encrypted secret that is being used in some form by applications or machines contains
     the right values or not. Although it is very easy to decrypt stuff using aws-cli but it can get bit too much if you have to do it quite frequently.
     Hence, this script is a very basic python wrapper around the aws-cli calls using boto3. In order to use this script:
     
      1. Log in to aws if you have sso enabled for cli access, or if you use something like credulous make sure you have appropriate shell vars.
      1. Please set the AWS_DEFAULT_REGION
      1. Run the script.

      *How do I run this script?*
      
      Run ```python3 ./src/kms-decrypt.py -h ```
      
      The above command prints help for the script listing out the params that could be passed.
      
      ```python3 ./src/kms-decrypt.py -p -e '<encrypted-string-here>' ```
      
      If you don't select -p option the plaintext would be written to a file. If you do pass -p as an argument it would write the output to the screen.
      
      *NOTE:* This script in its current incarnation doesn't support context and token.. but will add soon.