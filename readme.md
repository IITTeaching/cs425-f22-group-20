# Setting up project | Group 20 Braeden Weaver, Kayla, Marelle

## Setting up docker
1. `docker pull postgres`
2. `docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres`
3. New terminal
4. `docker pull dpage/pgadmin4`
5. `docker run -p 5555:80 --name pgadmin -e PGADMIN_DEFAULT_EMAIL="EMAIL" -e PGADMIN_DEFAULT_PASSWORD="password" dpage/pgadmin4`
6. Web browser to url `http://localhost:5555`
7. Get container ID of the postgres instance by typing `docker ps` in a new terminal and looking for the image postgres
8. Go to terminal and type `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ID`, replace ID with the ID of your docker container running postgres
9. Add new server connection to the IP of the postgres database
10. Make a new Database named "Banking"
11. Run DDL script by right clicking on the Banking table and then clicking CREATE script
12. Paste ddl.sql into that, and press the play button

## Setting up python environment
1. Setup python venv, in vscode, you press f1 and type Pyton: Create environemnt (select venv)
2. In your terminal, type the following
# Windows
3. `py -m pip install sqlalchemy`
4. `py -m pip install pandas`
5. `py -m pip install psycopg2`
6. `py -m pip install numpy`
# Unix
3. `python3 -m pip install sqlalchemy`
4. `python3 -m pip install pandas`
5. `python3 -m pip install psycopg2`
6. `python3 -m pip install numpy`

## Modifying config.py
```py
database_name = 'Banking'
database_username = 'postgres'
database_password = 'password'
```
Please modify this file if you have change anything during setup!