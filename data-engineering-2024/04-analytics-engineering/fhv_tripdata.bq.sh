bq --location=US mk \
   --table trips_data_all.fhv_tripdata \
   fhv_tripdata.table_definition.json

bq --location=US load \
   --replace \
   --source_format=CSV \
   --schema fhv_tripdata.table_definition.json \
   --skip_leading_rows=1 \
   trips_data_all.fhv_tripdata \
   'gs://ingestion-zoomcamp-414922/fhv-tripdata-2019/*.csv.gz'