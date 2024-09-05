resource "random_string" "cloudflare_api_token" {
  length  = 40
  special = false
  upper   = true
  lower   = true
}

variable "cloudflare_api_token" {
  type    = string
  default = random_string.cloudflare_api_token.result
}