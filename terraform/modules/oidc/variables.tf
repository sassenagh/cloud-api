variable "project_name" {
  type        = string
  description = "Project base name"
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, prod)"
}

variable "github_user" {
  type        = string
  description = "GitHub username or org name"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository name"
}
