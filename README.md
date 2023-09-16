<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Valorant_logo_-_pink_color_version.svg/1200px-Valorant_logo_-_pink_color_version.svg.png" width="100" />
</div>

# Valorant Match Data Pipeline

This project contains an end-to-end AWS data pipeline that ingests my personal Valorant match data from an API, and transforms the data to visualise and analyse my stats.

## Table of Contents

- [Architecture](#architecture)
- [Visualisation](#visualisation)
- [Installation](#installation)

## Architecture

![Architecture diagram](docs/valorant_data_pipeline_architecture.png)

## Visualisation

_Note that dates are in UTC._

![Visualisation output](docs/example_visualisation.png)

## Installation

1. Clone the repository

```sh
git clone git@github.com:jack-white9/valorant-match-data.git
```

2. [Set up AWS credentials in the CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

3. Build `amd64` ETL docker images

```sh
# Build extract job image
cd src/etl/extract
docker buildx build --platform linux/amd64 . -t extract

# Build transform job image
cd src/etl/transform
docker buildx build --platform linux/amd64 . -t transform
```

4. Tag and push images to ECR

```sh
# Login to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com

# Tag images
docker tag <extract_image_id> <repository_uri>:extract
docker tag <transform_image_id> <repository_uri>:transform

# Push images
docker push <repository_uri>:extract
docker push <repository_uri>:transform
```

5. Deploy infrastructure to AWS

```sh
cd infrastructure
terraform init
terraform plan
terraform apply
```
