## Setting up project

# Setting up docker
1. `docker pull postgres`
2. `docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres`
3. New terminal
4. `docker pull dpage/pgadmin4`
5. `docker run -p 5555:80 pgadmin -e PGADMIN_DEFAULT_EMAIL="EMAIL" -e PGADMIN_DEFAULT_PASSWORD="password" dpage/pgadmin4`
6. Web browser to url `http://localhost:5555`
7. Go to terminal and type `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' HASH`, replace HASH with the hash of your docker container running postgres
8. Add new server connection to the IP of the postgres database
9. Run DDL script

# Setting up python environment
1. Setup python venv
2. `python3 -m pip install sqlalchemy`
3. `python3 -m pip install pandas`
4. `python3 -m pip install psycopg2`
5. `python3 -m pip install numpy`