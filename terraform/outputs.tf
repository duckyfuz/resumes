output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.s3_distribution.domain_name
}

output "resume_hash" {
  value = local.resume_hash
}
