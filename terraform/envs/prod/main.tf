module "s3" {
  source       = "../../modules/s3"
  project_name = var.project_name
  environment  = var.environment
}

module "parameter_store" {
  source       = "../../modules/ssm"
  project_name = var.project_name
  environment  = var.environment
}

module "service_accounts" {
  source       = "../../modules/iam"
  project_name = var.project_name
  environment  = var.environment
}

module "oidc" {
  source       = "../../modules/oidc"
  project_name = var.project_name
  environment  = var.environment
  github_user  = "sassenagh"             
  github_repo  = "cloud-api"      
}