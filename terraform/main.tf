terraform {
  cloud {
    organization = "kenf-hcp-org"

    workspaces {
      name = "RESUME_HOSTING_WORKSPACE_PLACEHOLDER"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "4.40.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-1"
}

provider "aws" {
  region = "us-east-1"
  alias  = "us-east-1"
}

provider "cloudflare" {
  # CLOUDFLARE_API_TOKEN is expected as an environment variable in actions
}

locals {
  resume_source      = "../resume.pdf"
  resume_json_source = "../resume.json"
}
