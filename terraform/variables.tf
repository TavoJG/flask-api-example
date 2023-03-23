variable "gcp_project_id" {
  type = string
}

variable "gcp_project_region" {
  type = string
}

variable "app_name" {
  type    = string
  default = "app-eureka"
}

variable "container_addr" {
  type = string
}

variable "stock_api_key" {
  type = string
}

variable "stock_api_url" {
  type = string
}

variable "db_name" {
  type = string
}

variable "db_conn_string" {
  type = string
}
