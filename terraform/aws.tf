locals {
  resume_source  = "../kennethgao_resume.pdf"
  formatted_time = formatdate("DDMMYY-hhmmZZZ", timestamp())
  resume_hash    = filesha256(local.resume_source)
  resume_key     = format("resume_%s.pdf", local.resume_hash)
  s3_origin_id   = "myS3Origin"
}
