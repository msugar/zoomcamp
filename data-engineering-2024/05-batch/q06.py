import pyspark
from pyspark. sql import SparkSession
from pyspark.sql import types
from pyspark.sql.functions import col

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

df_zones = spark.read\
    .option("header", "true") \
    .csv('taxi+_zone_lookup.csv')

df_join = df.join(df_zones, df_zones.LocationID == df.PULocationID)

df_join.createOrReplaceTempView('joined_table')

df_res = spark.sql(
    '''
    SELECT 
        Zone,
        Count(1) AS pickup_count
    FROM
        joined_table
    GROUP BY joined_table.Zone
    ORDER BY pickup_count
    LIMIT 1;
    '''
)

df_res.show()