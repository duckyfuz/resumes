locals {
  # Use a different project name for PR previews
  effective_project_name = var.pr_number == "" ? var.project_name : "${var.project_name}-pr-${var.pr_number}"
  
  # For PR previews, construct the domain as resume-xx.domain.com
  # Assuming var.domain_name is something like 'resume.kenf.dev'
  domain_parts = split(".", var.domain_name)
  base_domain  = join(".", slice(locals.domain_parts, 1, length(locals.domain_parts)))
  subdomain    = locals.domain_parts[0]
  
  effective_domain_name = var.pr_number == "" ? var.domain_name : "${locals.subdomain}-${var.pr_number}.${locals.base_domain}"
}

resource "cloudflare_pages_project" "resume_project" {
  account_id    = var.cloudflare_account_id
  name          = locals.effective_project_name
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
  domain       = locals.effective_domain_name
}
