locals {
  resume_source = "../kennethgao_resume.pdf"
  formatted_time = formatdate("DDMMYY-hhmmZZZ", timestamp())
  resume_key     = format("kennethgao_resume_CAA%s.pdf", local.formatted_time)
  s3_origin_id = "myS3Origin"
}
