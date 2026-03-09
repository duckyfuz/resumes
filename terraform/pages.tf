resource "cloudflare_pages_project" "resume_project" {
  account_id    = var.cloudflare_account_id
  name          = var.project_name
  production_branch = "main"

  # We use the build configuration purely to dictate the deployment directory, 
  # as CI/CD will place the generated files here before deployment
  build_config {
    build_command   = ""
    destination_dir = "public"
  }
}

resource "cloudflare_pages_domain" "resume_domain" {
  account_id   = var.cloudflare_account_id
  project_name = cloudflare_pages_project.resume_project.name
  domain       = var.domain_name
}
