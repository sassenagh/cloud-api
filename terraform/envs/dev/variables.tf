variable "project_name" {
  type        = string
  description = "Project name used for resources"
}

variable "environment" {
  type        = string
  description = "Environment name (dev/prod)"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "aws_profile" {
  type        = string
  description = "AWS CLI profile to use"
  default     = "default"
}