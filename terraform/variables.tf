variable "cloudflare_account_id" {
  description = "Cloudflare Account ID"
  type        = string
}

variable "cloudflare_zone_id" {
  description = "Cloudflare Zone ID where your domain is managed"
  type        = string
}

variable "domain_name" {
  description = "The custom domain for the resume (e.g. resume.yourdomain.com)"
  type        = string
  default     = "resume.example.com"
}

variable "project_name" {
  description = "The name of the Cloudflare Pages project"
  type        = string
  default     = "resume-hosting"
}
