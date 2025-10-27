
import yaml
import boto3

# Load configuration from YAML file
CONFIG_FILE = "glue_job_config.yaml"

with open(CONFIG_FILE, "r") as config_file:
    config = yaml.safe_load(config_file)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Create tables based on folder configurations
for folder_config in config['FOLDER_CONFIGS']:
    table_name = folder_config['DYNAMODB_TABLE']
    metadata_fields = folder_config['METADATA_FIELDS']

    # Define attribute definitions and key schema
    attribute_definitions = [
        {
            'AttributeName': metadata_fields[0],  # Use first field as primary key
            'AttributeType': 'S'  # Assuming string type
        }
    ]

    key_schema = [
        {
            'AttributeName': metadata_fields[0],
            'KeyType': 'HASH'  # Partition key
        }
    ]

    # Create the table
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Creating table: {table_name}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table {table_name} already exists.")

print("DynamoDB table creation script completed.")
