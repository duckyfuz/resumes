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
  key          = local.resume_key
  source       = local.resume_source
  content_type = "application/pdf"
}

resource "aws_s3_bucket_website_configuration" "example" {
  bucket = aws_s3_bucket.resume_bucket.id

  index_document {
    suffix = local.resume_key
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
        Resource  = "${aws_s3_bucket.resume_bucket.arn}/${local.resume_key}"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.allow_public_acl]
}
