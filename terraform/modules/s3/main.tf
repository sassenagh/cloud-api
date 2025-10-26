resource "aws_s3_bucket" "main" {
  bucket = "${var.project_name}-${var.environment}-bucket"

  tags = {
    Name        = "${var.project_name}-${var.environment}"
    Environment = var.environment
  }
}