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
- Now, go to new terminal and run below command

- To execute postgresql database related command to create database which will be used in project
```
docker-compose exec db psql -U postgres -c "CREATE DATABASE sheeban;"
```
```
docker-compose exec db psql -U postgres -c "\l"
```

- To execute django commands while running docker.
```
docker-compose exec web python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```

- Create a super user(admin with all accesses) (OPTION, you can create a normal user by going to signup page)
```
docker-compose exec web python manage.py createsuperuser
```

- **Note** : All above Docker commonds will run runs python django server which is connect to db (postgresql).
- Now everything is setup , let run docker container using below docker commands :

### Now everything is setup for docker,so To run django in docker container follow below docker command, it will run project and you can check website "http://localhost:8000/" and to load data on db "http://127.0.0.1:8000/save_csv_data" use just one or when you have deleted or removed all the data in db.
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
- Now run docker django related commands, this will update any django code db related changes in django and db
```
docker-compose exec web python manage.py makemigrations
```
```
docker-compose exec web python manage.py migrate
```
Now Run, Docker as Usual : 
```
docker-compose up
```
### Make sure to use below docker command after stop 
```
docker-compose down
```
