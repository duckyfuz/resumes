# provider "cloudflare" {
#   api_token = var.cloudflare_api_token
# }
resource "cloudflare_record" "acm_certificate_cname" {
  zone_id = local.cloudflare_zone_id
  comment = "${local.comment_prefix} - for AWS ACM certificate"
  name    = local.acm_certificate_record_name
  type    = local.acm_certificate_record_type
  content = local.acm_certificate_record_value
  ttl     = 3600
  proxied = false
}

resource "cloudflare_record" "cloudfront_to_resume_cname" {
  zone_id = local.cloudflare_zone_id
  comment = "${local.comment_prefix} - for cloudfront record"
  name    = "resume"
  type    = "CNAME"
  content = aws_cloudfront_distribution.s3_distribution.domain_name
  ttl     = 3600
  proxied = false
}
