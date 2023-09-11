terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.region
}

/* s3 */

resource "aws_s3_bucket" "raw_bucket" {
  bucket = "valorant-data-raw"

  tags = {
    Project = var.project
  }
}

resource "aws_s3_bucket" "curated_bucket" {
  bucket = "valorant-data-curated"

  tags = {
    Project = var.project
  }
}


/* lambda */
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "archive_file" "raw_lambda_archive" {
  type        = "zip"
  source_file = "${path.module}/../src/ingestion/main.py"
  output_path = "raw_lambda_function_payload.zip"
}

resource "aws_lambda_function" "raw_lambda_function" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "raw_lambda_function_payload.zip"
  function_name = "raw_valorant_ingestion"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "main.main"

  source_code_hash = data.archive_file.raw_lambda_archive.output_base64sha256

  runtime = "python3.10"
}

