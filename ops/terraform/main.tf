terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Remote state — bucket is created once manually (or via bootstrap script).
  backend "gcs" {
    bucket = "tk-22-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ─── Artifact Registry (Docker images) ─────────────────────────────────────────
resource "google_artifact_registry_repository" "tk22" {
  location      = var.region
  repository_id = "tk-22"
  format        = "DOCKER"
  description   = "TK-22 container images"

  labels = local.common_labels
}

# ─── Cloud Run — Control Runtime API ───────────────────────────────────────────
resource "google_cloud_run_v2_service" "control_api" {
  name     = "tk22-control-api-${var.environment}"
  location = var.region

  template {
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.environment == "production" ? 10 : 3
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/tk-22/control-api:${var.image_tag}"

      ports {
        container_port = 5000
      }

      env {
        name = "APP_ENV"
        value = var.environment
      }

      env {
        name = "LOG_LEVEL"
        value = var.log_level
      }

      # Secrets are injected via Secret Manager — never plain-text env vars in prod.
      dynamic "env" {
        for_each = var.secret_env_vars
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value.secret_name
              version = env.value.secret_version
            }
          }
        }
      }
    }
  }

  labels = local.common_labels
}

# Allow unauthenticated access only when explicitly enabled (default: false in production)
resource "google_cloud_run_service_iam_member" "public_invoker" {
  count    = var.allow_unauthenticated ? 1 : 0
  location = google_cloud_run_v2_service.control_api.location
  service  = google_cloud_run_v2_service.control_api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ─── Secret Manager — secrets referenced by Cloud Run ──────────────────────────
locals {
  common_labels = {
    project     = "tk-22"
    environment = var.environment
    managed-by  = "terraform"
  }

  secret_names = [
    "OPENAI_API_KEY",
    "DISCORD_WEBHOOK",
    "N8N_TK22_PR_WEBHOOK",
    "HELIUS_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_KEY",
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",
  ]
}

resource "google_secret_manager_secret" "app_secrets" {
  for_each  = toset(local.secret_names)
  secret_id = "tk22-${lower(replace(each.key, "_", "-"))}-${var.environment}"

  replication {
    auto {}
  }

  labels = local.common_labels
}
