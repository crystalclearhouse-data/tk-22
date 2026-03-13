variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for all resources"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment: development | staging | production"
  type        = string
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "environment must be one of: development, staging, production"
  }
}

variable "image_tag" {
  description = "Docker image tag to deploy (e.g. git SHA or 'latest')"
  type        = string
  default     = "latest"
}

variable "log_level" {
  description = "Application log level"
  type        = string
  default     = "INFO"
}

variable "allow_unauthenticated" {
  description = "Allow unauthenticated (public) access to the Cloud Run service. Set false in production."
  type        = bool
  default     = false
}


  description = "Map of env var name → Secret Manager secret reference"
  type = map(object({
    secret_name    = string
    secret_version = string
  }))
  default = {}
}
