# Week 6 Homework Answers

## Setup
In addition to following the [homework instructions](homework.md): 

- To download the test data file:
    ```console
    wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
    ```

- To create a virtual environment with the required dependencies for the `q0n.py` programs:
    ```console
    python3 -m venv .venv
    source .venv/bin/activate

    pip install -r requirements.txt
    ```

- To instal SDKMAN: https://sdkman.io/install

- To instal Java using SDKMAN (Spark runs on Java 8/11/17, and I decided to go with Java Temurin 11.0.22 as of 2024-04-08):
    ```console
    sdk instal java 11.0.22-tem
    ```

- To install Spark with SDKMAN (Spark 3.5.0 is latest version as of 2024-04-08): 
    ```console
    sdk install spark 3.5.0
    ```

- To make sure you have the proper environment variables set by SDKMAN for each installation:
    ```console
    source ~/.bashrc
    ```
    Or, alternatively, just open a new command-line terminal.

- To verify the Java installation:
    ```console
    which java
    java -version
    ```

- To verify the Spark installation:
    ```console
    echo $SPARK_HOME
    which spark-shell
    which pyspark
    which spark-submit

    EXAMPLES_JAR=$(realpath `find ${SPARK_HOME}/ -type f -iname spark-examples*.jar`)
    spark-submit --name spark-pi --class org.apache.spark.examples.SparkPi local://${EXAMPLES_JAR}
    ```
    For the last command, you should see a non-logging message that looks like "Pi is roughly" followed by a number.

- To run `pyspark` with the required packages so it can consume reacords from Kafka or Redpanda:
    ```console
    pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-streaming_2.12:3.5.0
    ```

- Don't forget to start Redpanda!
    ```console
    docker-compose up -d
    ```

## Question 1 - Redpanda version
- Commands
    ```console
    alias rpk="docker exec -ti redpanda-1 rpk"
    rpk version
    ```
- Answer
    ```
    v22.3.5 (rev 28b2443)
    ```

## Question 2 - Creating a topic
- Command
    ```console
    rpk topic create test-topic --partitions 2
    ```
- Answer
    ```
    TOPIC       STATUS
    test-topic  OK
    ```

## Question 3 - Connecting to the Kafka server
- Command
    ```console
    python q03.py
    ```
- Answer
    ```
    True
    ```

## Question 4 - Sending data to the stream
- Command
    ```console
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
    ```console
    rpk topic create green-trips

    python q05.py
    ```
- Answer
    ```
    Total used time: 63.44 seconds.
    ```

## Question 6 - Parsing the data
- Submit `q06a.before_parsing.py` to Spark with the required packages:
    ```console
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-streaming_2.12:3.5.0 q06a.before_parsing.py
    ```

- The last lines should look like this:
    ```
    ==============================
    First row without parsing: Row(key=None, value=bytearray(b'{"lpep_pickup_datetime": "2019-10-01 00:26:02", "lpep_dropoff_datetime": "2019-10-01 00:39:58", "PULocationID": 112, "DOLocationID": 196, "passenger_count": 1, "trip_distance": 5.88, "tip_amount": 0.0}'), topic='green-trips', partition=0, offset=0, timestamp=datetime.datetime(2024, 4, 8, 14, 5, 55, 65000), timestampType=0)
    ==============================
    ```

- Now submit `q06b.after_parsing.py`:
    ```console
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-streaming_2.12:3.5.0 q06b.after_parsing.py
    ```

- This time, the last lines should look like this:
    ```
    ==============================
    First row with parsing: Row(lpep_pickup_datetime='2019-10-01 00:26:02', lpep_dropoff_datetime='2019-10-01 00:39:58', PULocationID=112, DOLocationID=196, passenger_count=1.0, trip_distance=5.88, tip_amount=0.0)
    ==============================
    ```

- Answer
    - Before parsing:
        ```
        Row(key=None, value=bytearray(b'{"lpep_pickup_datetime": "2019-10-01 00:26:02", "lpep_dropoff_datetime": "2019-10-01 00:39:58", "PULocationID": 112, "DOLocationID": 196, "passenger_count": 1, "trip_distance": 5.88, "tip_amount": 0.0}'), topic='green-trips', partition=0, offset=0, timestamp=datetime.datetime(2024, 4, 8, 14, 5, 55, 65000), timestampType=0)
        ```
    - Afer parsing:
        ```
        Row(lpep_pickup_datetime='2019-10-01 00:26:02', lpep_dropoff_datetime='2019-10-01 00:39:58', PULocationID=112, DOLocationID=196, passenger_count=1.0, trip_distance=5.88, tip_amount=0.0)
        ```

## Question 7 - Most popular destination
- Command
    ```console
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-streaming_2.12:3.5.0 q07.py
    ```
    The results should look like this:
    ```
    -------------------------------------------
    Batch: 0
    -------------------------------------------
    +------------------------------------------+------------+-----+
    |window                                    |DOLocationID|count|
    +------------------------------------------+------------+-----+
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|74          |17741|
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|42          |15942|
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|41          |14061|
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|75          |12840|
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|129         |11930|
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|7           |11533|
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|166         |10845|
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|236         |7913 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|223         |7542 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|238         |7318 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|82          |7292 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|181         |7282 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|95          |7244 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|244         |6733 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|61          |6606 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|116         |6339 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|138         |6144 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|97          |6050 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|49          |5221 |
    |{2024-04-08 14:40:00, 2024-04-08 14:45:00}|151         |5153 |
    +------------------------------------------+------------+-----+
    only showing top 20 rows    
    ```

- Answer
    ```
    The most popular destination was the one with `DOLocationID=74` 
    ```
