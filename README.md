# Sheeban-Wasi-Full-stack
# django-docker Setup
- As name suggest, this is Python Django web framework which runs on docker container.
- There is two docker files named **Dockerfile** and **docker-compose.yml**
- There is also django webapp which scrapes whatever URL you were provided in input field.

### Commands needed to run :
- GO to your project folder and run below to build docker first 
```
docker build .
```
- To create container
```
docker-compose up
```
```
contrl + C 
```
- To execute postgresql database related command to create database which will be used in project
```
docker-compose exec db psql -U postgres -c "CREATE DATABASE sheeban;"
```
```
docker-compose exec db psql -U postgres -c "\l""
```

- To execute django commands while running docker.
```
docker-compose exec web python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```
```
docker exec django-docker_web_1 python manage.py migrate
```
- Create a super user(admin with all accesses) (OPTION, you can create a normal user by going to signup page)
```
docker exec django-docker_web_1 python manage.py createsuperuser
```

- **Note** : All above Docker commonds will run runs python django server which is connect to db (postgresql).
- Now everything is setup , let run docker container using below docker commands :

### To run django in docker container , it will run project and you can check website "http://localhost:8000/"
```
docker-compose up
```
### Make sure to use below docker command after stop 
```
docker-compose down
```
