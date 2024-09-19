from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

def fun(query_text,csv_file):
    # Create SparkSession
    spark = SparkSession.builder.master("local[1]").appName("SparkByExamples.com").getOrCreate()
    if csv_file=='Exe_file_csv':
        hdfs_path = "hdfs://mfg:9000/csv/2/Exe_file_csv"
    elif csv_file=='Url_csv':
        hdfs_path = "hdfs://mfg:9000/csv/2/Url_csv"
    else:
        hdfs_path = "hdfs://mfg:9000/csv/data.csv"
    

    # Load DataFrame from CSV
    df = spark.read.option("header", True).csv(hdfs_path)
    
    # Rename columns and remove spaces (if any)
    newcols = [col(column).alias(column.replace(" ", "")) for column in df.columns]
    df = df.select(newcols)

    # Register DataFrame as a temporary view
    df.createOrReplaceTempView("df")

    # Show DataFrame information for debugging
    print("DataFrame Schema:")
    df.printSchema()
    print("Sample DataFrame Rows:")
    df.show(5)
    query_result = spark.sql(query_text)
    print("Query Result:")
    query_result.show(5)
    print("Received query:", query_text)
    # No need to return query_result since it's already shown
    pandas_df = query_result.toPandas()
    html_content = pandas_df.to_html()

    return html_content
