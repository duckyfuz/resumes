locals {
    cloudflare_zone_id = "47e2c26d25d25ff12cb21a0b2a5e1a4d"
}

resource "cloudflare_record" "cloudfront_to_resume_cname" {
  zone_id = local.cloudflare_zone_id
  comment = "CREATED BY TERRAFORM - for cloudfront record"
  name    = "resume"
  type    = "CNAME"
  content   = aws_cloudfront_distribution.s3_distribution.domain_name
  ttl     = 3600
  proxied = false
}
