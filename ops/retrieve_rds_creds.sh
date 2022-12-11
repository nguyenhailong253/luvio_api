#!/bin/bash
# https://medium.com/@codingmaths/bin-bash-what-exactly-is-this-95fc8db817bf

{ read -d'\n' DB_USERNAME DB_PASSWORD DB_HOST DB_PORT DB_NAME; } < <(aws secretsmanager get-secret-value --secret-id realestate-db-creds --region ap-southeast-2 --output json | jq -r '.SecretString' | jq -r '.username, .password, .host, .port, .dbname')
export DB_USERNAME DB_PASSWORD DB_HOST DB_PORT DB_NAME

django_env_file=".env"

echo "DB_USERNAME=$DB_USERNAME" > "$django_env_file"
echo "DB_PASSWORD=$DB_PASSWORD" >> "$django_env_file"
echo "DB_HOST=$DB_HOST" >> "$django_env_file"
echo "DB_PORT=$DB_PORT" >> "$django_env_file"
echo "DB_NAME=$DB_NAME" >> "$django_env_file"
echo "DB_SCHEMA=luvio" >> "$django_env_file"