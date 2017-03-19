#!/usr/bin/env python3

import docker
temp_file_location = "/tmp/docker-images"
save_images = ["aws-sso", "alpine"]


##############################################################################
def write_to_file(text):
    f = open(temp_file_location, 'w')
    f.write(text)
    f.close()


##############################################################################
def main():
    # create the docker client
    client = docker.from_env()

    # get all the images from docker daemon -> docker images
    docker_images = client.images.list()

    # now what do we do when we have more than one of anything ??
    # obviously loop.
    for image in docker_images:
        # Now if only this docker library listed the freaking name of the freaking image
        # sigh !! lets do some crazy shenanigans.
        # all is not lost. Name can be found in the repo tags in the attrs list.
        repo_tag = image.attrs['RepoTags'][0].split(":")[0]

        can_delete_image = True
        for image_to_save in save_images:
            if image_to_save in repo_tag:
                can_delete_image = False
                print("Repo Tag matches image you asked to save")

        # checking if this image is aws-sso image (whole point of this script)
        if can_delete_image:
            try:
                print("Deleting image {} {}".format(repo_tag, "banana"))
                client.images.remove(image.short_id, force=True, noprune=True)
            except Exception as e:
                print("Exception raised while deleting image {}".format(repo_tag))
                print(str(e))

if __name__ == '__main__':
    main()