provider "aws" {
  region = "ap-southeast-1"
}

provider "aws" {
  region = "us-east-1"
  alias = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "resume-storage-bucket"
    key    = "terraform/key"
    region = "ap-southeast-1"
  }
}

locals {
  resume_source = "../kennethgao_resume.pdf"
  s3_origin_id = "myS3Origin"
}

resource "aws_s3_bucket" "resume_bucket" {
  bucket = "resume-storage-bucket"
}

resource "aws_s3_bucket_public_access_block" "allow_public_acl" {
  bucket = aws_s3_bucket.resume_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_object" "pdf_upload" {
  bucket       = aws_s3_bucket.resume_bucket.bucket
  key          = "kennethgao_resume.pdf"
  source       = local.resume_source
  content_type = "application/pdf"
}

resource "aws_s3_bucket_website_configuration" "example" {
  bucket = aws_s3_bucket.resume_bucket.id

  index_document {
    suffix = "kennethgao_resume.pdf"
  }
}

resource "aws_s3_bucket_policy" "resume_bucket_policy" {
  bucket = aws_s3_bucket.resume_bucket.bucket

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.resume_bucket.arn}/kennethgao_resume.pdf"
      }
    ]
  })

  depends_on = [ aws_s3_bucket_public_access_block.allow_public_acl ]
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name              = aws_s3_bucket.resume_bucket.bucket_regional_domain_name
    origin_id                = local.s3_origin_id
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "kennethgao_resume.pdf"

  aliases = ["resume.kenf.dev"]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  # Cache behavior for PDF files
  ordered_cache_behavior {
    path_pattern     = "/kennethgao_resume.pdf"
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate_validation.cert.certificate_arn
    ssl_support_method = "sni-only"
  }
}

resource "aws_acm_certificate_validation" "cert" {
  provider = aws.us-east-1
  certificate_arn         = "arn:aws:acm:us-east-1:533267177082:certificate/af022575-6c3d-4075-96f1-52911405fdd4"
}
