output "control_api_url" {
  description = "Public URL of the deployed Control Runtime API"
  value       = google_cloud_run_v2_service.control_api.uri
}

output "artifact_registry_url" {
  description = "Docker registry URL for TK-22 images"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/tk-22"
}

output "secret_ids" {
  description = "Secret Manager secret IDs provisioned for this environment"
  value       = { for k, v in google_secret_manager_secret.app_secrets : k => v.secret_id }
}
