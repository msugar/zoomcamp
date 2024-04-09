import time

import pyspark
from pyspark.sql import SparkSession

pyspark_version = pyspark.__version__
kafka_jar_package = f"org.apache.spark:spark-sql-kafka-0-10_2.12:{pyspark_version}"

spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("GreenTripsConsumer") \
    .config("spark.jars.packages", kafka_jar_package) \
    .getOrCreate()
    
spark.sparkContext.setLogLevel("WARN")
    
green_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "green-trips") \
    .option("startingOffsets", "earliest") \
    .load()

def peek(mini_batch, batch_id):
    first_row = mini_batch.take(1)
    if first_row:
        print('=' * 30)
        print(f"First row without parsing: {first_row[0]}")
        print('=' * 30)

query = green_stream.writeStream.foreachBatch(peek).start()

time.sleep(10)

query.stop()
