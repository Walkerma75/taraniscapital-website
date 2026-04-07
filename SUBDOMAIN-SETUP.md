# Subdomain Setup Guide — Fund Sites

This guide covers deploying the four fund subdomain sites on AWS (S3 + CloudFront), plus removing the old biotech redirect from the CloudFront function.

---

## Step 0: Remove /biotech/ Redirect from CloudFront Function

The `url-rewrite` function currently redirects `/biotech/` to `biotech.taraniscapital.com`. This needs removing so `/biotech` serves the new sector page on the main site.

```bash
# 1. Get the current function code and ETag
aws cloudfront get-function --name url-rewrite --stage LIVE --output json > cf-function.json

# 2. Extract just the function code to a file
aws cloudfront get-function --name url-rewrite --stage LIVE --query 'FunctionCode' --output text > url-rewrite.js

# 3. Edit url-rewrite.js — find and DELETE the biotech redirect block:
#    Look for something like:
#      if (uri === '/biotech' || uri === '/biotech/') {
#        return { statusCode: 301, ... location: { value: 'https://biotech.taraniscapital.com' } ... }
#      }
#    Remove those lines entirely.

# 4. Get the ETag (needed for update)
ETAG=$(aws cloudfront describe-function --name url-rewrite --query 'ETag' --output text)

# 5. Update the function
aws cloudfront update-function \
  --name url-rewrite \
  --function-config Comment="URL rewrite and redirects - biotech redirect removed",Runtime=cloudfront-js-2.0 \
  --function-code fileb://url-rewrite.js \
  --if-match $ETAG

# 6. Publish (get new ETag first)
ETAG=$(aws cloudfront describe-function --name url-rewrite --query 'ETag' --output text)
aws cloudfront publish-function --name url-rewrite --if-match $ETAG
```

---

## Step 1: Request Wildcard SSL Certificate

One certificate covers all subdomains. Must be in us-east-1 for CloudFront.

```bash
aws acm request-certificate \
  --domain-name "*.taraniscapital.com" \
  --subject-alternative-names "taraniscapital.com" \
  --validation-method DNS \
  --region us-east-1
```

This outputs a CertificateArn. Note it down, e.g.: `arn:aws:acm:us-east-1:ACCOUNT:certificate/XXXX`

Add the DNS validation CNAME record to Route 53:

```bash
# Get the validation CNAME details
aws acm describe-certificate \
  --certificate-arn YOUR_CERT_ARN \
  --region us-east-1 \
  --query 'Certificate.DomainValidationOptions[0].ResourceRecord'

# Add the CNAME to Route 53 (replace NAME and VALUE from above)
aws route53 change-resource-record-sets \
  --hosted-zone-id Z0680053Y587NB8B8C9S \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "_VALIDATION_NAME",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "_VALIDATION_VALUE"}]
      }
    }]
  }'
```

Wait for certificate to be ISSUED (usually 5-10 minutes):
```bash
aws acm wait certificate-validated --certificate-arn YOUR_CERT_ARN --region us-east-1
```

---

## Step 2: Create S3 Buckets (one per subdomain)

```bash
# Create buckets
for SUBDOMAIN in fintech datacentre property disruptive-tech; do
  aws s3 mb s3://${SUBDOMAIN}.taraniscapital.com --region eu-west-2
done

# Enable static website hosting
for SUBDOMAIN in fintech datacentre property disruptive-tech; do
  aws s3 website s3://${SUBDOMAIN}.taraniscapital.com \
    --index-document index.html \
    --error-document 404.html
done

# Set public read bucket policy
for SUBDOMAIN in fintech datacentre property disruptive-tech; do
  aws s3api put-bucket-policy \
    --bucket ${SUBDOMAIN}.taraniscapital.com \
    --policy "{
      \"Version\": \"2012-10-17\",
      \"Statement\": [{
        \"Sid\": \"PublicReadGetObject\",
        \"Effect\": \"Allow\",
        \"Principal\": \"*\",
        \"Action\": \"s3:GetObject\",
        \"Resource\": \"arn:aws:s3:::${SUBDOMAIN}.taraniscapital.com/*\"
      }]
    }"
done
```

---

## Step 3: Upload Fund Sites to S3

From the repo root (where the subdomains/ folder is):

```bash
cd "C:\Users\mark\Claude Cowork\Taranis Capital Website"

for SUBDOMAIN in fintech datacentre property disruptive-tech; do
  aws s3 sync subdomains/${SUBDOMAIN}/ s3://${SUBDOMAIN}.taraniscapital.com/ --delete
done
```

---

## Step 4: Create CloudFront Distributions

Create one distribution per subdomain. Replace `YOUR_CERT_ARN` with the wildcard cert ARN from Step 1.

```bash
for SUBDOMAIN in fintech datacentre property disruptive-tech; do
  aws cloudfront create-distribution \
    --distribution-config "{
      \"CallerReference\": \"${SUBDOMAIN}-taranis-$(date +%s)\",
      \"Origins\": {
        \"Quantity\": 1,
        \"Items\": [{
          \"Id\": \"S3-${SUBDOMAIN}.taraniscapital.com\",
          \"DomainName\": \"${SUBDOMAIN}.taraniscapital.com.s3-website.eu-west-2.amazonaws.com\",
          \"CustomOriginConfig\": {
            \"HTTPPort\": 80,
            \"HTTPSPort\": 443,
            \"OriginProtocolPolicy\": \"http-only\"
          }
        }]
      },
      \"DefaultCacheBehavior\": {
        \"TargetOriginId\": \"S3-${SUBDOMAIN}.taraniscapital.com\",
        \"ViewerProtocolPolicy\": \"redirect-to-https\",
        \"AllowedMethods\": {\"Quantity\": 2, \"Items\": [\"HEAD\", \"GET\"]},
        \"CachedMethods\": {\"Quantity\": 2, \"Items\": [\"HEAD\", \"GET\"]},
        \"ForwardedValues\": {\"QueryString\": false, \"Cookies\": {\"Forward\": \"none\"}},
        \"MinTTL\": 0,
        \"DefaultTTL\": 86400,
        \"MaxTTL\": 31536000,
        \"Compress\": true
      },
      \"Aliases\": {\"Quantity\": 1, \"Items\": [\"${SUBDOMAIN}.taraniscapital.com\"]},
      \"ViewerCertificate\": {
        \"ACMCertificateArn\": \"YOUR_CERT_ARN\",
        \"SSLSupportMethod\": \"sni-only\",
        \"MinimumProtocolVersion\": \"TLSv1.2_2021\"
      },
      \"Comment\": \"Taranis Capital ${SUBDOMAIN} fund site\",
      \"Enabled\": true,
      \"DefaultRootObject\": \"index.html\",
      \"HttpVersion\": \"http2\",
      \"PriceClass\": \"PriceClass_100\"
    }" \
    --query 'Distribution.DomainName' \
    --output text
done
```

Note down each distribution's CloudFront domain (e.g. `d1234abcdef.cloudfront.net`).

---

## Step 5: Add Route 53 CNAME Records

For each subdomain, point it to the corresponding CloudFront distribution domain:

```bash
# Replace CF_DOMAIN with the actual CloudFront domain from Step 4

# Fintech
aws route53 change-resource-record-sets \
  --hosted-zone-id Z0680053Y587NB8B8C9S \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "fintech.taraniscapital.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "CF_DOMAIN_FINTECH"}]
      }
    }]
  }'

# Datacentre
aws route53 change-resource-record-sets \
  --hosted-zone-id Z0680053Y587NB8B8C9S \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "datacentre.taraniscapital.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "CF_DOMAIN_DATACENTRE"}]
      }
    }]
  }'

# Property
aws route53 change-resource-record-sets \
  --hosted-zone-id Z0680053Y587NB8B8C9S \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "property.taraniscapital.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "CF_DOMAIN_PROPERTY"}]
      }
    }]
  }'

# Disruptive Tech
aws route53 change-resource-record-sets \
  --hosted-zone-id Z0680053Y587NB8B8C9S \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "disruptive-tech.taraniscapital.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "CF_DOMAIN_DISRUPTIVETECH"}]
      }
    }]
  }'
```

---

## Step 6: Verify

```bash
# Check DNS propagation
for SUBDOMAIN in fintech datacentre property disruptive-tech; do
  echo "=== ${SUBDOMAIN}.taraniscapital.com ==="
  nslookup ${SUBDOMAIN}.taraniscapital.com
done

# Check HTTPS (may take 15-30 mins for CloudFront deployment)
for SUBDOMAIN in fintech datacentre property disruptive-tech; do
  echo "=== ${SUBDOMAIN} ==="
  curl -sI https://${SUBDOMAIN}.taraniscapital.com | head -5
done
```

---

## Optional: GitHub Actions for Subdomain Deploys

To auto-deploy subdomain sites on push (like the main site), add to `.github/workflows/deploy.yml`:

```yaml
      - name: Deploy fintech subdomain
        run: aws s3 sync subdomains/fintech/ s3://fintech.taraniscapital.com/ --delete

      - name: Deploy datacentre subdomain
        run: aws s3 sync subdomains/datacentre/ s3://datacentre.taraniscapital.com/ --delete

      - name: Deploy property subdomain
        run: aws s3 sync subdomains/property/ s3://property.taraniscapital.com/ --delete

      - name: Deploy disruptive-tech subdomain
        run: aws s3 sync subdomains/disruptive-tech/ s3://disruptive-tech.taraniscapital.com/ --delete

      - name: Invalidate subdomain CloudFront caches
        run: |
          aws cloudfront create-invalidation --distribution-id CF_DIST_FINTECH --paths "/*"
          aws cloudfront create-invalidation --distribution-id CF_DIST_DATACENTRE --paths "/*"
          aws cloudfront create-invalidation --distribution-id CF_DIST_PROPERTY --paths "/*"
          aws cloudfront create-invalidation --distribution-id CF_DIST_DISRUPTIVETECH --paths "/*"
```

Replace `CF_DIST_*` with the actual CloudFront distribution IDs once created.
