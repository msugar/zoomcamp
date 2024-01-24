# Module 1 Homework Answers

## Environment
- Windows_NT x64 10.0.19045
- WSL 2.0.9.0
- Ubuntu 22.04.03 LTS
- Docker 24.0.7
- Python 3.10.12 
- Visual Studio Code 1.85.1

## Docker & SQL

### Question 1. Knowing docker tags 
Which tag has the following text? - *Automatically remove the container when it exits*

#### Procedure
```
docker run --help | grep 'Automatically remove the container when it exits'
```

#### Answer
`--rm`

### Question 2. Understanding docker first run
Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

#### Procedure
1. Interactive approach

    1.1 First, run the designated Docker container and ask it to start a Bash process
    ```
    docker run -it python:3.9 bash
    ```

    1.2 Then, run `pip list` inside Bash
    ```
    pip list --disable-pip-version-check | grep wheel
    ```

    1.3 When you're done, press `ctrl + D` to exit the Bash session and thus terminate the container.

2. Or, alternatively, the direct approach
    ```
    docker run --rm python:3.9 bash -c 'pip list --disable-pip-version-check' | grep wheel
    ```

#### Answer
`0.42.0`

### Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
```

You will also need the dataset with zones:

```
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline.)

#### Procedure

*Note:* I've changed `ingest_data.py` to suit my personal preferences.

1. (Optional) Download the data files:
    The ingestion program read the input files directly from their location on the Internet, so this step is optional. In case you want to take a look at the data yourself, which is always a good idea. 
    ```
    cd cohorts/2024/01-docker-terraform/2_docker_sql

    mkdir -p download

    wget -P $(pwd)/download https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz

    wget -P $(pwd)/download https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
    ```

2. Create a directory to persist the database data outside the container
    This is to preserve the database between Docker container runs. Note Postgress will change the ownership and access rights of this directory.
    ```
    mkdir -p ny_taxi_postgres_data
    ```

3. Create a Docker network so the containers can reach each other
    ```
    docker network create pg-network
    ```

4. Run Postgres DBMS server:
    ```
    docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --rm \
    --network=pg-network \
    --name pgdatabase \
      postgres:13
    ```

5. In another terminal, run Postgres Administration tool:
    ```
    docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --rm \
    --network=pg-network \
    --name pgadmin \
      dpage/pgadmin4
    ```
    
6. In a third terminal, build and run `ingest_data.py` to ingest the data from the downloaded files into the database:

    Note: `ingest_data.py` had originally a bug. It expected to find the `tpep_pickup_datetime` and `tpep_dropoff_datetime` columns, but the input file has `lpep_pickup_datetime` and `lpep_dropoff_datetime` instead.

    ```
    cd 01-docker-terraform/2_docker_sql

    docker build -t ingest_data:1 .

    docker run \
    -v $(pwd)/download:/download \
    --rm \
    --network=pg-network \
    --name ingest_data \
    ingest_data:1 \
    --user root \
    --password root \
    --host pgdatabase \
    --port 5432 \
    --db ny_taxi \
    --table_name ny_taxi_2019_09 \
    --url https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz \
    --if_table_exists replace \
    --datetime_fields lpep_pickup_datetime lpep_dropoff_datetime

    docker run \
    -v $(pwd)/download:/download \
    --rm \
    --network=pg-network \
    --name ingest_data \
    ingest_data:1 \
    --user root \
    --password root \
    --host pgdatabase \
    --port 5432 \
    --db ny_taxi \
    --table_name ny_zone \
    --url https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv \
    --if_table_exists replace
    ```
    
7. Using a Web browser, access the Postgres Administration tool now running on [http://localhost:8080](http://localhost:8080/login)

    After logging into the tool, `Add New Server` as follows:

    - General tab
      + Name: pgdatabase

    - Connection tab
      + Host name/address: pgdatabase
      + Username: root
      + Pasword: root
    
    - Save

### Question 3. Count records

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

#### Query
```
select count(1) as qty
from public.ny_taxi_2019_09
where lpep_pickup_datetime >= '2019-09-18 00:00:00'
  and lpep_dropoff_datetime < '2019-09-19 00:00:00'
```

#### Answer
`15612`

### Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance.
Use the pick up time for your calculations.

#### Query
```
select date(lpep_pickup_datetime)
from public.ny_taxi_2019_09
where trip_distance = (
  select max(trip_distance) from public.ny_taxi_2019_09
)
```
or
```
select date(lpep_pickup_datetime)
from public.ny_taxi_2019_09
order by trip_distance desc
limit 1
```

#### Answer
`2019-09-26`

### Question 5. The number of passengers
Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

#### Query
```
select z."Borough" as borough, sum(t.total_amount) as sum_total_amount
from public.ny_taxi_2019_09 as t
left join public.ny_zone as z 
  on t."PULocationID" = z."LocationID"
where t.lpep_pickup_datetime >= '2019-09-18 00:00:00'
  and t.lpep_dropoff_datetime < '2019-09-19 00:00:00'
  and z."Borough" <> 'Unknown'
group by 1
having sum(t.total_amount) > 50000
order by 2 desc
```
 
#### Answer
`"Brooklyn" "Manhattan" "Queens"`

### Question 6. Largest tip
For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

#### Query
```
select do_z."Zone" as dropoff_zone, max(t.tip_amount) as largest_tip_amount
from public.ny_taxi_2019_09 as t
left join public.ny_zone as pu_z 
  on t."PULocationID" = pu_z."LocationID"
left join public.ny_zone as do_z 
  on t."DOLocationID" = do_z."LocationID"
where t.lpep_pickup_datetime >= '2019-09-01 00:00:00'
  and t.lpep_dropoff_datetime < '2019-10-01 00:00:00'
  and pu_z."Zone" = 'Astoria'
group by 1
order by 2 desc
limit 1
```

#### Answer
`JFK Airport`

### (Optional) Cleanup (after you have got all the answers, of course)

*Beware:* These commands will delete all Docker containers, volumes, and networks, as well as the Postgres database!

```
docker rm -f $(docker ps -a -q)

docker volume rm $(docker volume ls -q)

docker network prune --force

sudo rm -fr download ny_taxi_postgres_data
```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


### Question 7. Creating Resources

#### Procedure

*Note:* I've changed the `*.tf` files a bit by removing the sensitive values I don't want to expose in GitHub. I also named the bucket after the project ID, to get an easy unique name. I know there are other ways, but this is just a lab so let's keep things simple.

Make sure you have your GCP credentials properly set, and your current GCP configuration points to the project of your choice:
```shell
gcloud auth list

gcloud config list
```

Feel free to change the `variable.tf` file. But don't keep any sensitive information in it, if you intend to check your changes in the version control repository (e.g., in GitHub). 

Instead, prefer to create a `tfvars` file to set the value of the `project` (and any other) variable. Note that `.gitignore` is already set to exclude all `*.tfvars` files from version control.

Example `lab.tfvars`:
```
project = "<insert here your GCP project ID>"
```

Run the Terraform commands to create the resources in your GCP project:
```shell
cd 01-docker-terraform/1_terraform_gcp/terraform

terraform init

terraform plan -var-file=lab.tfvars

terraform apply -var-file=lab.tfvars
```

Paste the output of this command into the homework submission form.

Don't forget to delete those resources after your work, to avoid costs on any running services:
```shell
terraform destroy -var-file=lab.tfvars
```

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used

Deadline: 29 January, 23:00 CET 