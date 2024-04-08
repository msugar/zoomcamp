import time 
import gzip
import json
import csv
from kafka import KafkaProducer


# Kafka producer configuration
producer_config = {
    'bootstrap_servers': 'localhost:9092', # Adjust this to your Kafka server address
    'value_serializer': lambda v: json.dumps(v).encode('utf-8')
}

# Initialize Kafka producer
producer = KafkaProducer(**producer_config)

# Function to process and send records to Kafka
def send_to_kafka(record):
    # Extract required columns
    extracted_record = {
        'lpep_pickup_datetime': record['lpep_pickup_datetime'],
        'lpep_dropoff_datetime': record['lpep_dropoff_datetime'],
        'PULocationID': int(record['PULocationID']),
        'DOLocationID': int(record['DOLocationID']),
        'passenger_count': int(record['passenger_count'] or "0"),
        'trip_distance': float(record['trip_distance']),
        'tip_amount': float(record['tip_amount'])
    }
    # Send to Kafka topic
    producer.send('green-trips', extracted_record)
    
# Record the start time
start_time = time.time()

# Read and process the gzipped CSV file
with gzip.open('green_tripdata_2019-10.csv.gz', 'rt') as file:
    csvobj = csv.DictReader(file)
    for record in csvobj:
        send_to_kafka(record)

# Ensure all messages are sent
producer.flush()
producer.close()

# Record the time ended
end_time = time.time()

# Calculate execution time
time_used = end_time - start_time

# Print the execution time
print(f'Total used time: {time_used:.2f} seconds.')