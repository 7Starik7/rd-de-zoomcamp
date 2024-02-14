variable "credentials" {
  description = "Credentials"
  default     = "../../gcp-keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "rd-de-course"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "Big Query dataset name"
  default     = "rd_de_course_dataset"
}

variable "gcs_storage_bucket_name" {
  description = "Bucket Storage name"
  default     = "rd-de-course-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage class"
  default     = "STANDART"
}