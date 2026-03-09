resource "cloudflare_record" "resume_cname" {
  zone_id = var.cloudflare_zone_id
  name    = var.domain_name
  type    = "CNAME"
  
  # Point the custom domain directly to the Pages project's generated dev domain
  content = "${cloudflare_pages_project.resume_project.name}.pages.dev"
  
  # Proxied is necessary for standard Cloudflare CDN to cache and protect the pages site
  proxied = true
  ttl     = 1
}
