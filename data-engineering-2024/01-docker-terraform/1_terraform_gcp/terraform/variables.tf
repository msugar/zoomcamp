variable "project" {
  description = "Project ID"
  nullable = false
}

variable "region" {
  description = "Region"
  # Update the below to your desired region
  default     = "northamerica-northeast1" # Montreal
}

variable "bq_location" {
  description = "BigQuery Location"
  # Update the below to your desired GCS location
  default     = "northamerica-northeast1" # Montreal
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  # Update the below to what you want your dataset to be called
  default     = "w01_demo"
}

variable "gcs_location" {
  description = "Bucket Location"
  # Update the below to your desired GCS location
  default     = "NORTHAMERICA-NORTHEAST1" # Montreal
}

variable "gcs_bucket_name_suffix" {
  description = "Bucket Name suffix. Together with the project ID, it will make an unique bucket name."
  # Update the below to your desired GCS bucket name suffix.
  default     = "w01_demo"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}