# Module 2 Homework Answers

## Workflow Orchestration with Mage

### "API to Postgress" Mage Pipeline

#### Procedure

1. Read [mage-zoomcamp/README.md](https://github.com/mage-ai/mage-zoomcamp/blob/master/README.md) to know how to stand up Mage and Postgres using Docker Compose.

1. Watch the recommended videos (like [DE Zoomcamp 2.2.3 - ETL: API to Postgres](https://www.youtube.com/watch?v=Maidfe7oKLs)) to learn how to build an ETL pipeline in Mage. 

1. Using Mage, build and run the `green_taxi_etl` pipeline as described in [homework.md](homework.md). Note the date columns of the [green taxi dataset](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download) start with `l` instead of `t`:
    ```
    # native date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    ```

### Question 1. Data Loading

Once the dataset is loaded, what's the shape of the data?

#### Answer
* 266,855 rows x 20 columns

### Question 2. Data Transformation

Upon filtering the dataset where the passenger count is greater than 0 _and_ the trip distance is greater than zero, how many rows are left?

#### Answer
* 139,370 rows

### Question 3. Data Transformation

Which of the following creates a new column `lpep_pickup_date` by converting `lpep_pickup_datetime` to a date?

* `data = data['lpep_pickup_datetime'].date`
* `data('lpep_pickup_date') = data['lpep_pickup_datetime'].date`
* `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`
* `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt().date()`

#### Answer
* `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`

### Question 4. Data Transformation

What are the existing values of `VendorID` in the dataset?

#### Answer
* 1 or 2

### Question 5. Data Transformation

How many columns need to be renamed to snake case?

#### Answer
* 4

### Question 6. Data Exporting

Once exported, how many partitions (folders) are present in Google Cloud?

#### Answer
* 95

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw2
* Check the link above to see the due date
