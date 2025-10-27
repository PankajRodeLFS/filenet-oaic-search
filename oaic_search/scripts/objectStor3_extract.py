
import sys
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3

# Get job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'CONFIG_FILE'])

# Initialize Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load configuration from JSON file
with open(args['CONFIG_FILE'], 'r') as config_file:
    config = json.load(config_file)

s3_bucket_name = config['S3_BUCKET_NAME']
dynamodb_table_name = config['DYNAMODB_TABLE_NAME']
metadata_fields = config['METADATA_FIELDS']

s3_input_path = f"s3://{s3_bucket_name}/metadata/"

# Read JSON files from S3
df = spark.read.json(s3_input_path)

# Select searchable fields
metadata_df = df.select(*metadata_fields)

# Convert to Python objects for DynamoDB
metadata_list = metadata_df.collect()

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

# Write each record to DynamoDB
for row in metadata_list:
    item = {}
    for field in metadata_fields:
        value = row[field]
        if isinstance(value, list):
            item[field] = ','.join(value)
        else:
            item[field] = value
    table.put_item(Item=item)

print(f"Inserted {len(metadata_list)} items into DynamoDB.")

job.commit()
