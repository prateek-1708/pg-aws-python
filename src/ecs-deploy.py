#!/usr/bin/python3

import boto3
import argparse
import pprint
import sys


##############################################################################
def debug(args):
    print('Cluster Name: {}'.format(args.cluster))
    print('Service Name: {}'.format(args.service))
    print('Image Version: {}'.format(args.image_version))


##############################################################################
def die(message='I am dying...'):
    print("Error: {}".format(message))
    sys.exit(1)


##############################################################################
def debug_and_die():
    debug()
    die()


##############################################################################
def get_client(client_type):
    try:
        return boto3.client(client_type)
    except:
        die('Cannot call boto3.client...')


##############################################################################
def search_and_return_arn_from_haystack(haystack, key, needle):
    arns = haystack[key]
    match = [arn for arn in arns if needle in arn]
    arn = match.pop()
    return arn


##############################################################################
def read_arguments():

    parser = argparse.ArgumentParser("Deploy Docker image to ecs cluster")
    parser.add_argument(
        "-c",
        "--cluster",
        required=True,
        dest="cluster",
        help="Cluster name where this docker image needs to be deployed"
    )
    parser.add_argument(
        "-s",
        "--service",
        required=True,
        dest="service",
        help="Service name where this docker image needs to be deployed"
    )
    parser.add_argument(
        "-i",
        "--image-version",
        required=True,
        dest="image_version",
        help="Version of the image to be deployed"
    )

    args = parser.parse_args()

    if not args.cluster:
        parser.error("Cluster name is required in order for this to work")

    if not args.service:
        parser.error("Service name is required in order for this to work")

    if not args.image_version:
        parser.error("Image version is required in order to do the deploy")

    return parser.parse_args()


##############################################################################
def main():

    args = read_arguments()
    cluster_name_to_search = args.cluster
    service_name_to_search = args.service
    debug(args)

    # create the kms client to do the decrypttion
    ecs_client = get_client('ecs')

    # Getting the cluster
    clusters = ecs_client.list_clusters()
    cluster_arn = search_and_return_arn_from_haystack(clusters, 'clusterArns', cluster_name_to_search)

    # Getting the services
    services = ecs_client.list_services(cluster=cluster_arn)
    service_arn = search_and_return_arn_from_haystack(services, 'serviceArns', service_name_to_search)

    # describing the service
    service_details = ecs_client.describe_services(cluster=cluster_arn, services=[service_arn])
    task_definition_arn = ((service_details['services']).pop())['taskDefinition']

    task_def_details = ecs_client.describe_task_definition(taskDefinition=task_definition_arn)

    task_definition = task_def_details['taskDefinition']
    print(task_definition)

    family = task_definition['family']
    print(family)

    volumes = task_definition['volumes']

    container_definition = task_definition['containerDefinitions'][0]
    print(container_definition)

    image = container_definition['image']
    print(image)

    split_array = image.split("/")
    image_name_and_tag = split_array[1].split(":")

    new_image_name_and_tag = image_name_and_tag[0] + ":" + args.image_version
    repo_and_image_name_with_tag = split_array[0] + "/" + new_image_name_and_tag

    container_definition['image'] = repo_and_image_name_with_tag

    response = ecs_client.register_task_definition(
        family=family,
        containerDefinitions=[container_definition],
        volumes=volumes
    )
    pprint.pprint(response)
    pprint.pprint(response['taskDefinition']['taskDefinitionArn'])

    deployed = ecs_client.update_service(
        cluster=cluster_arn,
        service=service_arn,
        taskDefinition=response['taskDefinition']['taskDefinitionArn']
    )
    pprint.pprint(deployed)


##############################################################################
if __name__ == '__main__':
    main()