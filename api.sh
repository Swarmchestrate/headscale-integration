#!/bin/bash

set -e

DOMAIN="https://headscale-test.swarmchestrate.sztaki.hu"

API_KEY="4ooBucA.GWYiRhrUrkOEE1f5Q8bRTastQRi0agIH"

echo "Enter username:"
read USERNAME

if [ -z "$USERNAME" ]; then
    echo "Username cannot be empty"
    exit 1
fi

echo ""
echo "=== GET API: /api/v1/user ==="
echo "Checking if the user exists"
echo ""

USER_RESPONSE=$(curl -s \
  -X GET "$DOMAIN/api/v1/user" \
  -H "Authorization: Bearer $API_KEY")

USER_ID=$(echo "$USER_RESPONSE" | jq -r ".users[] | select(.name==\"$USERNAME\") | .id")

if [ -z "$USER_ID" ] || [ "$USER_ID" == "null" ]; then

    echo "=== POST API: /api/v1/user ==="
    echo "Creating new user: $USERNAME"

    USER_RESPONSE=$(curl -s \
      -X POST "$DOMAIN/api/v1/user" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"name\":\"$USERNAME\"}")

    USER_ID=$(echo "$USER_RESPONSE" | jq -r '.user.id')

else
    echo "User already exists"
fi

if [ -z "$USER_ID" ] || [ "$USER_ID" == "null" ]; then
    echo "Could not get user ID"
    exit 1
fi


KEY_RESPONSE=$(curl -s \
  -X POST "$DOMAIN/api/v1/preauthkey" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
        \"user\": $USER_ID,
        \"reusable\": true
      }")

JOIN_KEY=$(echo "$KEY_RESPONSE" | jq -r '.preAuthKey.key')
echo ""
echo "=== POST API: /api/v1/preauthkey ==="
echo " Generating pre-auth key.."
echo "$JOIN_KEY"

if [ -z "$JOIN_KEY" ] || [ "$JOIN_KEY" == "null" ]; then
    echo "Failed to generate pre-auth key"
    exit 1
fi

echo ""
echo "====================================="
echo "Headscale user: $USERNAME"
echo ""
echo "K3s flag:"
echo "--vpn-auth=name=tailscale,joinKey=$JOIN_KEY,controlServerURL=$DOMAIN"
echo ""
echo "====================================="