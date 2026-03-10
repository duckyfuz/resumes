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
}

variable "project_name" {
  description = "The name of the Cloudflare Pages project"
  type        = string
}

variable "pr_number" {
  description = "The number of the pull request for preview environments"
  type        = string
  default     = ""
}
