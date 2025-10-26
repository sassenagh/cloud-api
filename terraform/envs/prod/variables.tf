variable "aws_region" {
  description = "AWS region for this environment"
  type        = string
}

variable "aws_profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "default"
}

variable "environment" {
  description = "Environment name (dev, prod, etc.)"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
}
