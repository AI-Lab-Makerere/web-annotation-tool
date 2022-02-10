# How to setup the Annotation T using Docker

**Assumption:** it's assumed that you have cloned this repository onto your server or desktop pc.

There are 2 ways to setup using docker i.e Create and manage your own image OR Pull and use image maintained by AIR Makerere. 

### OPTION 1: CREATE AND MAINTAIN YOUR OWN IMAGE

#### 1. Install the Docker runtime environment on your desktop or server

   - Windows : Download and install docker desktop from [here](https://hub.docker.com/editions/community/docker-ce-desktop-windows) 
   - Linux:  follow this [article](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
   - Mac: Download and install docker desktop from [here](https://www.docker.com/products/docker-desktop)

#### 2. Build Docker image

   - Before building your image that will eventually be deployed, there are some configurations/settings that you need to personalize in the system
   - One of them is setting the email credentials for the mail server to enable smooth sending of emails. 
   - Create a .env file by renaming the example.env file at the root of the project and set your email credentials and other defaults for the following variables `DEFAULT_FROM_EMAIL, EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD` `,EMAIL_PORT, ALLOWED_HOSTS (here add your server ip and domain to the list), SECRET_KEY (you can generate a new secret key) ` 
   - You can also open the Dockerfile at the root of the project and see if you need to modify anything say the port on which you want the application containers to be exposed at. You can make any other code related changes to the project at this stage before creating the actual image. 
   - Next move on to building the docker image for the project: navigate to the project root and run the following command `docker build . -t <name-the-image:tag-name>` E.g `docker build . -t annotator:v1` 

#### 3. Run Docker container

   - On first time run, you need to create a superuser account using the code snipper below: 
   ```
    docker run -it -p 8020:8020 \
     -e DJANGO_SUPERUSER_USERNAME=adminusername \
     -e DJANGO_SUPERUSER_PASSWORD=youradminpassword \
     -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
    <image-name:tag-name>
```


    Replace <image-name:tag-name> with your image details for the image you created e.g annotaion:v1

    The command tells Docker to run the container and forward the exposed port 8020 to port 8020 on your local machine. With -e we set environment variables that automatically create an admin user.



  - Once you have set up the admin account, you can stop and re-run the containers in the background. Use `Ctr + c` to stop the currently running container. 
  - To run the container in the background run the following command `docker run -p 8020:8020 <image-name:tag-name>`

#### 4. Push your image to Dockerhub

  - This is an optional step that helps to make your image accessible for use/deployment accross other platforms like cloud providers e.g AWS, GCP etc or your servers running docker. 
  - First create an account with [dockerhub](https://hub.docker.com/signup) in case you don't have one and then [create a repository on dockerhub](https://docs.docker.com/docker-hub/repos/) having the same name as your image e.g annotation based on this write up. 
  - You retag your already built image to match the dockerhub `username/repo:tag-name` format using the command 
  ```
  docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]

  E.g docker tag annotaion:v1 mydockerUsername/annotation:v1
```
  - Login to dockerhub via your terminal using the command `docker login` it will prompt you to enter your Dockerhub username and password
  - Finally push your image to dockerhub through the command `docker push mydockerUsername/annotation:v1`
  - Login to dockerhub and check that your repository has the pushed image. 








### OPTION 2: USE IMAGE MAINTATINED  BY AIR MAKERERE 

##### 1. Pull the image 
  - From your server or pc having docker installed, pull the image of the annotion tool using the command `docker pull airlabmakerere/annotation-tool:latest` 
  
#### 2. Run image containers

   - On first time run, you need to create a superuser account using the code snipper below: 
   ```
    docker run -it -p 8020:8020 \
     -e DJANGO_SUPERUSER_USERNAME=adminusername \
     -e DJANGO_SUPERUSER_PASSWORD=youradminpassword \
     -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
    <image-name:tag-name>
```


    Replace <image-name:tag-name> with your image details for the image you created e.g annotaion:v1

    The command tells Docker to run the container and forward the exposed port 8020 to port 8020 on your local machine. With -e we set environment variables that automatically create an admin user.



  - While still in the terminal, update the .env file at the root directory. Nano into .env through `nano .env` then update the following environment variables:  `DEFAULT_FROM_EMAIL, EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD` `,EMAIL_PORT, ALLOWED_HOSTS (here add your server ip and domain to the list), SECRET_KEY (you can generate a new secret key) ` 
  - Once you have set up the admin account, you can stop and re-run the containers in the background. Use `Ctr + c` to stop the currently running container. 
  - To run the container in the background run the following command `docker run -p 8020:8020 <image-name:tag-name>`