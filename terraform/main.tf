provider "aws" {
  region = "ap-southeast-1"
}

provider "aws" {
  region = "us-east-1"
  alias  = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "resume-storage-bucket"
    key    = "terraform/key"
    region = "ap-southeast-1"
  }

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4"
    }
  }
}
