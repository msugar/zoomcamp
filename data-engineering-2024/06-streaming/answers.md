# Week 6 Homework Answers

## Setup
 - Follow the homework instructions. 
 - Download the test data file:
    ```
    wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
    ```
 - Create a virtual environment with the required dependencies:
    ```
    python3 -m venv .venv
    source .venv/bin/activate

    pip install -r requirements.txt
    ```
 
## Question 1 - Redpanda version
- Commands
    ```
    alias rpk="docker exec -ti redpanda-1 rpk"
    rpk version
    ```
- Answer
    ```
    v22.3.5 (rev 28b2443)
    ```

## Question 2 - Creating a topic
- Command
    ```
    rpk topic create test-topic --partitions 2
    ```
- Answer
    ```
    TOPIC       STATUS
    test-topic  OK
    ```

## Question 3 - Connecting to the Kafka server
- Commands
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install kafka-python

    python q03.py
    ```
- Answer
    ```
    True
    ```
## Question 4 - Sending data to the stream
- Command
    ```
    python q04.py
    ```
- Answer
    ```
    Sent: {'number': 0}
    Sent: {'number': 1}
    Sent: {'number': 2}
    Sent: {'number': 3}
    Sent: {'number': 4}
    Sent: {'number': 5}
    Sent: {'number': 6}
    Sent: {'number': 7}
    Sent: {'number': 8}
    Sent: {'number': 9}
    took 0.53 seconds
    ```
    Out of that, because of the `sleep()` function calls, at least 0.50 seconds were spent sending the messages.
## Question 5 - Sending the Trip Data
- Command
    ```
    python q05.py
    ```
- Answer
    ```
    Total used time: 63.44 seconds.
    ```

## Question 6 - Parsing the data
- Command
    ```
    # Spin up an environment with Docker containers for the Spark Master, Spark Worker, and Repanda
    docker-compose -f docker-compose.spark.yml up --detach

    # Remote into the Spark master node
    SPARK_MASTER_CONTAINER=$(docker ps --format "{{.Names}}" | grep master)
    docker exec -i -t $SPARK_MASTER_CONTAINER /bin/bash

    # Test Spark is working
    EXAMPLES_JAR=$(realpath `find . -type f -iname spark-examples*.jar`)
    ./bin/spark-submit --master spark://spark-master:7077 --name spark-pi --class org.apache.spark.examples.SparkPi local://${EXAMPLES_JAR}
    # You should see a non-logging message that starts with "Pi is roughly" and a number.

    # Make sure you can see the files outside the container
    ls -la /mounted-data/*.py

    # Shutdown the Spark cluster
    docker-compose -f docker-compose.spark.yml down
    ```
- Troubleshooting

    If you get the following error when you run `pyspark`:
    ```
    Error: pyspark does not support any application options.
    ```
    use this [workaround](https://github.com/bitnami/containers/issues/38139):
    ```
    sed -i '$ d' bin/pyspark
    echo 'exec "${SPARK_HOME}"/bin/spark-submit pyspark-shell-main "$@"' >> bin/pyspark
    ```
- Answer
    - Before parsing:
        ```
        Row(key=None, value=bytearray(b'{"lpep_pickup_datetime":"2019-10-06 10:34:04","lpep_dropoff_datetime":"2019-10-06 10:41:03","PULocationID":97,"DOLocationID":33,"passenger_count":1,"trip_distance":1.31,"tip_amount":1.0}'), topic='green-trips', partition=0, offset=794036, timestamp=datetime.datetime(2024, 3, 25, 15, 30, 20, 461000), timestampType=0)
        ```
    - Afer parsing:
        ```
        Row(lpep_pickup_datetime='2019-10-04 17:57:52', lpep_dropoff_datetime='2019-10-04 18:10:24', PULocationID=185, DOLocationID=51, passenger_count=1.0, trip_distance=3.28, tip_amount=0.0)
        ```
        
## Question 7 - Most popular destination
- Answer
    ```
    The most popular destination was the one with `DOLocationID=74` 
    ```
