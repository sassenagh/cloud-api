resource "aws_ssm_parameter" "api_url" {
  name  = "/${var.project_name}/${var.environment}/api_url"
  type  = "String"
  value = "https://${var.project_name}-${var.environment}.example.com"
}

resource "aws_ssm_parameter" "db_connection" {
  name  = "/${var.project_name}/${var.environment}/db_connection"
  type  = "SecureString"
  value = "postgres://user:password@db:5432/app"
}

resource "aws_ssm_parameter" "version" {
  name  = "/${var.project_name}/${var.environment}/version"
  type  = "String"
  value = "v1.0.0"
}
