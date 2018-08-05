import docker
import tarfile
import urllib.request
import subprocess
import os
import time

max_retries = 2
count = 1

class DeployError(Exception):
    pass

def shell(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0]

def download_from_s3():
    print("Downloading images from s3")
    destination_folder = "public/images"
    file_name = "pandapics.tar.gz"
    url = "https://s3.eu-central-1.amazonaws.com/devops-exercise/{0}".format(file_name)
    if not os.path.isdir(destination_folder):
        os.makedirs(destination_folder)
    stream_data = urllib.request.urlopen(url)
    tar_data = tarfile.open(fileobj=stream_data, mode="r|gz")
    tar_data.extractall(destination_folder)

def docker_build():
    try:
        print("Building Images")
        docker_client = docker.from_env()
        print("Building node application image")
        docker_client.build(".", "opspython2:latest", quiet=True, rm=True)
        print("Building DB image")
        docker_client.build("db", "opspython2-db:latest", quiet=True, rm=True)
    except Exception as e:
        print(e)

def compose_up():
    try:
        print("Running docker-compose up")
        shell("/usr/local/bin/docker-compose up -d")
    except Exception as e:
        print(e)

def check_status_code():
    global count
    global max_retries
    print("Test application HealthCheck, {0}/{1}".format(count, max_retries))
    health_check_url = "http://localhost:3000/health"
    try:
        res = urllib.request.urlopen(health_check_url)
        if res.status == 200:
            print("Successfully deployed bigpanda test application")
        else:
            destroy_deployment()
            raise DeployError("Application didn't pass healthcheck")
    except Exception as e:
        print("HealthCheck failed, retrying to let containers start")
        count += 1
        if count <= max_retries:
            print("Retry HealthCheck in 2 seconds due to connection error")
            time.sleep(2)
            check_status_code()
        else:
            destroy_deployment()
            print("HealthCheck didn't pass tests, {0}".format(e))

def destroy_deployment():
    print("Removing containers")
    try:
        shell("/usr/local/bin/docker-compose stop")
        shell("/usr/local/bin/docker-compose rm -f")
    except Exception as e:
        print(e)

def main():
    download_from_s3()
    docker_build()
    compose_up()
    check_status_code()

if __name__ == "__main__":
    main()
