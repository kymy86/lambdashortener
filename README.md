# AWS serverless URL shortener ![version][version-badge]

[version-badge]: https://img.shields.io/badge/version-0.1-blue.svg

This is a serverless URL shortener app, built by using the [Zappa Framework].

[Zappa Framework]:  https://github.com/Miserlou/Zappa

## Quick Start

1. Run the **lambdashortener.yml** CloudFormation template to provisions the required AWS services. It returns two outputs: the S3 bucket url and the bucket name.
2. Set-up the **zappa_settings.yml** with two environment variables:
    - BUCKET_URL: The bucket url returned back by the CloudFormation template
    - BUCKET_NAME: The bucket name returned back by the CloudFormation template
3. Run **zappa deploy prod** command