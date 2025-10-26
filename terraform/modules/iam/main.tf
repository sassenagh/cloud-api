resource "aws_iam_role" "service_role" {
  name = "${var.project_name}-${var.environment}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "access_policy" {
  name        = "${var.project_name}-${var.environment}-policy"
  description = "Allow access to S3 and SSM for ${var.project_name}"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.service_role.name
  policy_arn = aws_iam_policy.access_policy.arn
}
