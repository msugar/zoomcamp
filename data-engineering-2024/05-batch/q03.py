import pyspark
from pyspark. sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F

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

df = df.withColumn('pickup_date', F.to_date(df.pickup_datetime))

df.createOrReplaceTempView("fhv_data")

oct15_count = df.select('pickup_date').filter(df.pickup_date == '2019-10-15').count()

print(f"{oct15_count=}")