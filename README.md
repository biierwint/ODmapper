# ODmapper - Omics Data Mapping and Harmonizer
ODmapper is used to map a genomic variant to the OMOP concept_id (particularly OMOP Genomic) through API call based on Django REST framework.
In a nutshell, a user can use the API to query the "CONCEPT" and "CONCEPT_SYNONYM" of OMOP CDM tables based on the query text (concept_id, concept_synonym, concept_name and concept_code).

ODmapper has been packaged as docker containers.

## Setting up seqrepo
Please follow the instructions here: https://github.com/biocommons/biocommons.seqrepo
Please ensure that the seqrepo directory is at /usr/local/share/seqrepo/

If you setup seqrepo follow the instructions above, then you can skip this part.
### Manual downloading of "seqrepo.tar.gz"
1. Download seqrepo.tar.gz
2. Extract the file "seqrepo.tar.gz" to "/usr/local/share/". It should appear as /usr/local/share/seqrepo/
(Note: You need to ensure that you have read permission to "/usr/local/share/seqrepo/")

## Setting up ODmapper and the supporting docker instances
### Step 1: Navigate to odmapper_api/ folder
```
cd odmapper_api/
```

### Step 2: Run docker compose
Copy the .env.example file to .env file. Subsequently, please edit .env file to suit your system.
If your deployment is not in the local server, please ensure that you modify the "DJANGO_ALLOWED_HOSTS" in the ".env" file.

Run:
```
source .env
```

Then run docker compose:
```
docker compose up --build
```

### Step 3: Setting up database
In a separate terminal, navigate to the "ODmapper" folder.
Then execute below commands:
```
gunzip -c database-setup.sql.gz | docker exec -i odmapper_api-odmapper-postgres-1 psql -U postgres
gunzip -c odmapper_database_dump.sql.gz | docker exec -i odmapper_api-odmapper-postgres-1 psql -U postgres -d odmapper
```

### Step 4: Create initial migrations for database tables
```
docker exec -i odmapper python manage.py makemigrations
docker exec -i odmapper python manage.py migrate
```

### Step 5: Create superuser
```
docker exec -it odmapper python manage.py createsuperuser
(Key-in your username, password, and email address accordingly)
```

### Step 6: Test your deployment
If you test your deployment from the same server:
- Go to a browser and go to URL: "http://localhost:8000/" to test if ODmapper is successfully deployed.
- Go to a browser and go to URL: "http://localhost:5000/" to test if seqrepo-rest-service is successfully deployed.

If you test your deployment from another server, please ensure that you have modified the "DJANGO_ALLOWED_HOSTS" in the ".env" file.
Otherwise, please stop the docker compose. Then modify the .env file and run "docker compose up --build" again. Then open browser and go to URL: http://<your deployment server IP address>:8000/

## TIPS
Once you have built the containers, you do not need to build it again unless there are changes to your programs.
To start the containers:
```
docker compose up
```

To start the containers in background:
```
docker compose up --detach
```

To check the logs:
```
docker compose logs
```

To login to the container
```
docker exec -it <container_name> sh
```
For example: 
```
docker exec -it odmapper_api-odmapper-postres-1 sh
```
