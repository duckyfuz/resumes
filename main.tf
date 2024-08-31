provider "aws" {
  region = "ap-southeast-1"
}

terraform {
  backend "s3" {
    bucket = "resume-storage-bucket"
    key    = "terraform/key"
    region = "ap-southeast-1"
  }
}

resource "aws_s3_bucket" "resume_bucket" {
  bucket = "resume-storage-bucket"
  tags = {
    Name        = "Resume Storage Bucket"
    Environment = "Production"
  }
}

resource "aws_s3_object" "pdf_upload" {
  bucket = aws_s3_bucket.resume_bucket.bucket
  key    = "kennethgao_resume.pdf"
  source = "kennethgao_resume.pdf"
  acl    = "private"
}
