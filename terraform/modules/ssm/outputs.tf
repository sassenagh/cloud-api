output "parameter_names" {
  value = [
    aws_ssm_parameter.api_url.name,
    aws_ssm_parameter.db_connection.name,
    aws_ssm_parameter.version.name
  ]
}
