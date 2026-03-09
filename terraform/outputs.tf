output "pages_project_domain" {
  description = "The generated default domain for the Cloudflare Pages project"
  value       = "${cloudflare_pages_project.resume_project.name}.pages.dev"
}

output "custom_domain_url" {
  description = "The custom domain where the resume will be hosted"
  value       = "https://${var.domain_name}"
}
