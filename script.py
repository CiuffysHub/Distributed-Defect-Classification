'''# SCRIPT NUMBER 1
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
# Sc = SparkContext() # should already be available
sqlContext = SQLContext(sc)
spark.read.csv("hdfs://testbed-master:9000/fortune500dataset.csv")'''

# SCRIPT NUMBER 2
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext.getOrCreate()
spark = SparkSession(sc)
from pyspark.ml.clustering import KMeans
df = spark.read.format("image").option("dropInvalid", True).load("hdfs://testbed-master:9000/good/359*.jpeg")
df.select("image.origin", "image.width", "image.height").show(truncate=False)
kmeans = KMeans(k=2)

import pyspark.sql.functions as F
from pyspark.ml.image import ImageSchema
from pyspark.ml.linalg import DenseVector, VectorUDT

ImageSchema.imageFields

img2vec = F.udf(lambda x: DenseVector(ImageSchema.toNDArray(x).flatten()), VectorUDT())

df = df.withColumn('vecs', img2vec("image"))
new_df = df.select("vecs").withColumnRenamed("vecs","features").select("features")
model = kmeans.fit(new_df)
output=model.transform(new_df)
output.show()

df = spark.read.format("image").option("dropInvalid", True).load("hdfs://testbed-master:9000/test.jpg")

ImageSchema.imageFields

img2vec = F.udf(lambda x: DenseVector(ImageSchema.toNDArray(x).flatten()), VectorUDT())

df = df.withColumn('vecs', img2vec("image"))
new_df = df.select("vecs").withColumnRenamed("vecs","features").select("features")
output=model.transform(new_df)
output.show()