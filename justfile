DOCKERHUB_USERNAME := "rlmflores"
IMAGE_NAME := "simple-web-server"

# Define a recipe to build the Docker image
build:
    docker build -t {{IMAGE_NAME}} .

# Define a recipe to run the Docker container
run:
    docker run -p 5000:5000 {{IMAGE_NAME}}

# Define a recipe to stop the Docker container
stop:
    docker stop $(docker ps -q --filter ancestor={{IMAGE_NAME}})

# Define a recipe to remove the Docker container
remove:
    docker rm $(docker ps -a -q --filter ancestor={{IMAGE_NAME}})

# Define a recipe to rebuild and run the Docker container
rebuild: stop remove build run

# Define a recipe to tag the Docker image
tag:
    docker tag {{IMAGE_NAME}} {{DOCKERHUB_USERNAME}}/{{IMAGE_NAME}}:latest

# Define a recipe to push the Docker image to Docker Hub
push: tag
    docker push {{DOCKERHUB_USERNAME}}/{{IMAGE_NAME}}:latest