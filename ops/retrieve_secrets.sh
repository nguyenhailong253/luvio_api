#!/bin/bash
# https://medium.com/@codingmaths/bin-bash-what-exactly-is-this-95fc8db817bf

{ read -d'\n' DB_USERNAME DB_PASSWORD DB_HOST DB_PORT; } < <(aws secretsmanager get-secret-value --secret-id realestate-db-creds --region ap-southeast-2 --output json | jq -r '.SecretString' | jq -r '.username, .password, .host, .port')
{ read -d'\n' AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY STATIC_PUB_S3_BUCKET DB_NAME DB_SCHEMA DOMAIN_API_CLIENT_ID DOMAIN_API_CLIENT_SECRET DOMAIN_API_SCOPE; } < <(aws secretsmanager get-secret-value --secret-id luvio-api-secrets --region ap-southeast-2 --output json | jq -r '.SecretString' | jq -r '.aws_access_key_id, .aws_secret_access_key, .static_public_s3_bucket, .dbname, .dbschema, .domain_api_client_id, .domain_api_client_secret, .domain_api_scope')
export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY STATIC_PUB_S3_BUCKET DB_USERNAME DB_PASSWORD DB_HOST DB_PORT DB_NAME DB_SCHEMA DOMAIN_API_CLIENT_ID DOMAIN_API_CLIENT_SECRET DOMAIN_API_SCOPE

django_env_file=".env"

echo "DB_USERNAME=$DB_USERNAME" > "$django_env_file"
echo "DB_PASSWORD=$DB_PASSWORD" >> "$django_env_file"
echo "DB_HOST=$DB_HOST" >> "$django_env_file"
echo "DB_PORT=$DB_PORT" >> "$django_env_file"
echo "DB_NAME=$DB_NAME" >> "$django_env_file"
echo "DB_SCHEMA=$DB_SCHEMA" >> "$django_env_file"

# For luvio backend user account
echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> "$django_env_file"
echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> "$django_env_file"
echo "STATIC_PUB_S3_BUCKET=$STATIC_PUB_S3_BUCKET" >> "$django_env_file"

echo "DOMAIN_API_CLIENT_ID=$DOMAIN_API_CLIENT_ID" >> "$django_env_file"
echo "DOMAIN_API_CLIENT_SECRET=$DOMAIN_API_CLIENT_SECRET" >> "$django_env_file"
echo "DOMAIN_API_SCOPE=$DOMAIN_API_SCOPE" >> "$django_env_file"

{ read -d'\n' DOMAIN_API_TOKEN; } < <(curl -X POST -u "$DOMAIN_API_CLIENT_ID:$DOMAIN_API_CLIENT_SECRET" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=client_credentials&scope=$DOMAIN_API_SCOPE" 'https://auth.domain.com.au/v1/connect/token' | jq -r '.access_token')
export DOMAIN_API_TOKEN
echo "DOMAIN_API_TOKEN=$DOMAIN_API_TOKEN" >> "$django_env_file"
