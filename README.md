# Sheeban-Wasi-Full-stack
# django-docker Setup
- As name suggest, this is Python Django web framework which runs on docker container.
- There is two docker files named **Dockerfile** and **docker-compose.yml**
- There is also django webapp which scrapes whatever URL you were provided in input field.

### Commands needed to run :
- GO to your project folder and run below to build docker first , this will add your project to docker and create web and database docker image
```
docker build .
```
- To create container and make required changes for django 
```
docker-compose up
```
- Create a super user(admin with all accesses) by going to this link when you run server (OPTION, you can create a normal user by going to signup page)
```
http://127.0.0.1:8000/create_admin
```

- **Note** : All above Docker commonds will run runs python django server which is connect to db (postgresql).
- Now everything is setup , let run docker container using below docker commands :

### Now everything is setup for docker,so To run django in docker container follow below docker command, it will run project and you can check website "http://localhost:8000/" and to load data on db "http://127.0.0.1:8000/save_db_data" or you can click load_Sample_data when you login as admin.
```
docker-compose up
```
### Make sure to use below docker command after stop 
```
docker-compose down
```

### To Update code (In Case, you have already created docker Image and NOw you want to update code in the docker Image) 
```
docker build .
```
or 
- Below is for in case you put a specific name to docker image manually
```
docker build <image-name> .
```
Now Run, Docker as Usual : 
```
docker-compose up
```
### Make sure to use below docker command after stop 
```
docker-compose down
```
