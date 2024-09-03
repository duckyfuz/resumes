# provider "cloudflare" {
#   api_token = var.cloudflare_api_token
# }

locals {
    cloudflare_zone_id = "47e2c26d25d25ff12cb21a0b2a5e1a4d"
}

resource "cloudflare_record" "cloudfront_to_resume_cname" {
  zone_id = local.cloudflare_zone_id
  name    = "resume"
  type    = "CNAME"
  content   = "d1qf0qghsqyx1z.cloudfront.net"  # TODO: replace with var from aws.tf
  ttl     = 3600
  proxied = false
}
