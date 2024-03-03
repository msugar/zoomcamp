import pyspark
from pyspark. sql import SparkSession
from pyspark.sql import types

spark = SparkSession. builder\
    .master( "local" ) \
    .appName( "homework" ) \
    .getOrCreate( )

schema = types.StructType([
    types.StructField('dispatching_base_num', types.StringType(), True), 
    types.StructField('pickup_datetime', types.TimestampType(), True), 
    types.StructField('dropoff_datetime', types.TimestampType(), True), 
    types.StructField('PULocationID', types.IntegerType(), True), 
    types.StructField('DOLocationID', types.IntegerType(), True), 
    types.StructField('SR_Flag', types.StringType(), True),
    types.StructField('Affiliated_base_number', types.StringType(), True)
])

df = spark.read\
    .option("header","true")\
    .schema(schema)\
    .csv('fhv_tripdata_2019-10.csv.gz')

print(f"{df.schema=}")

df = df.repartition(numPartitions=6)

df.write.parquet('q02_output/')