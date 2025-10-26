terraform {
  backend "s3" {
    bucket         = "my-terraform-states"
    key            = "prodl/terraform.tfstate"
    region         = "eu-west-1"
    use_lockfile   = true
    encrypt        = true
  }
}

