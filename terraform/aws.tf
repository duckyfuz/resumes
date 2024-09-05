locals {
  resume_source  = "../kennethgao_resume.pdf"
  formatted_time = formatdate("DDMMYY-hhmmZZZ", timestamp())
  resume_key     = format("resume_%s.pdf", filesha256(local.resume_source))
  s3_origin_id   = "myS3Origin"
}
