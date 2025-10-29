output "github_actions_role_arn" {
  description = "IAM Role ARN for GitHub OIDC"
  value       = aws_iam_role.github_actions.arn
}
output "oidc_provider_arn" {
  description = "IAM OIDC Provider ARN for GitHub"
  value       = aws_iam_openid_connect_provider.github.arn
}
