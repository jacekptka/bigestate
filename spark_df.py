#job for EMR


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import Row

spark = SparkSession.builder \
    .appName('DataFrame') \
    .master('local[*]') \
    .getOrCreate()

#df = spark.read.load("s3://jpi-bigestate/estates_krakow_10_0.json", format="json")
df = spark.read.format("csv").option("header", "true").load("s3://jpi-bigestate/estates_krakow_1_?.json")
df.agg({" Cena" : "avg"}).show()

#df.show()



