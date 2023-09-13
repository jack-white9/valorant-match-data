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

resource "aws_s3_bucket" "raw" {
  bucket = "valorant-data-raw"

  tags = {
    Project = var.project
  }
}

resource "aws_s3_bucket" "curated" {
  bucket = "valorant-data-curated"

  tags = {
    Project = var.project
  }
}

resource "aws_s3_bucket" "lambda_package" {
  bucket = "valorant-lambda-packages"

  tags = {
    Project = var.project
  }
}


/* lambda */
module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "raw_valorant_ingestion"
  description   = "Ingests raw Valorant match data into S3"
  handler       = "main.main"
  runtime       = "python3.10"
  publish       = true
  timeout       = 90
  store_on_s3   = true
  s3_bucket     = aws_s3_bucket.lambda_package.id

  source_path = [
    {
      path = "${path.module}/../src/ingestion/",

      poetry_install = true
    }
  ]

  environment_variables = {
    PUUID  = "2ecce5c6-6d31-579c-bf56-bf6743e19270",
    REGION = "ap"
  }

  tags = {
    Project = var.project
  }
}
