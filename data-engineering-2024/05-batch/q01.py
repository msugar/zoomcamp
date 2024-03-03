import pyspark
from pyspark. sql import SparkSession

spark = SparkSession. builder\
    .master( "local" ) \
    .appName( "homework" ) \
    .getOrCreate( )

print(f"{spark.version=}")