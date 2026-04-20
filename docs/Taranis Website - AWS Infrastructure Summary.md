# Taranis Capital Website — AWS & Infrastructure Summary

## Overview

The main Taranis Capital website (taraniscapital.com) is a static HTML/CSS/JS site hosted on AWS, with automated deployment via GitHub Actions. There is no backend infrastructure, CMS, or database — it is a flat-file static site only.

## AWS Services in Use

**S3 (Simple Storage Service)**
- Bucket name: `taraniscapital.com`
- Region: `eu-west-2` (London)
- Static website hosting is enabled with a public read bucket policy
- This is the origin store for all site files (HTML, CSS, JS, images, fonts)

**CloudFront (CDN)**
- Distribution ID: `E18AUIFBUGMXSB`
- Domain: `d1ete5r3431epc.cloudfront.net`
- Sits in front of the S3 website endpoint for caching and HTTPS
- A CloudFront Function handles clean URL routing (appends `.html` to extensionless paths, so `/contact` serves `contact.html`)

**DNS & SSL**
- Custom domain (`taraniscapital.com`) and SSL certificate are configured, pending final validation

## CI/CD Pipeline

- **Source control:** GitHub — repository `Walkerma75/taraniscapital-website`
- **Deployment:** GitHub Actions workflow (`.github/workflows/deploy.yml`) triggers on every push to the `main` branch
- **Pipeline steps:** S3 sync (uploads changed files) → CloudFront cache invalidation (clears CDN cache so changes go live immediately)
- **Credentials:** AWS access keys are stored as encrypted secrets in the GitHub repository settings

## What's Currently on the Site

- Corporate pages: Home, Who We Are, Our Approach, Our Funds, Insights, Contact, Privacy Policy, Cookie Policy
- Individual profile pages for 9 team members and 18 board advisers
- Fund detail pages: Fintech, Biotech, Datacentres, Property, Disruptive Tech
- Contact form handling is external (MailerLite — no AWS involvement)
- Insights page aggregates RSS feeds client-side (no server processing)

## What Is NOT in Place

There is currently no backend or application-layer infrastructure. Specifically, none of the following are set up:

- Lambda (serverless functions)
- API Gateway
- DynamoDB or any other database
- Cognito (authentication/user management)
- IAM roles beyond the S3/CloudFront deployment credentials
- VPC, EC2, or any compute resources

Any application functionality (e.g. a dataroom) would need to be built from scratch on top of the existing AWS account and domain.
