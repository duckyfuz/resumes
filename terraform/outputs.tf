output "pages_project_domain" {
  description = "The generated default domain for the Cloudflare Pages project"
  value       = cloudflare_pages_project.resume_project.subdomain
}

output "effective_domain_name" {
  description = "The domain name where the resume is currently hosted"
  value       = local.effective_domain_name
}

output "custom_domain_url" {
  description = "The custom domain where the resume will be hosted"
  value       = "https://${local.effective_domain_name}"
}
