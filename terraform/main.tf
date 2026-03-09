terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  # CLOUDFLARE_API_TOKEN is expected as an environment variable in actions
}

locals {
  resume_source      = "../resume.pdf"
  resume_json_source = "../resume.json"
}
