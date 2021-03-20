#!/bin/sh

# Making a directory for storing dependencies and removing the old one
sudo rm -r package
sudo mkdir package

# Downloading other dependencies
sudo -H /usr/bin/python3.6 -m pip install -r requirements.txt --target ./package

# Packaging dependencies
cd package
zip -r ../sms-sender-dependencies.zip .

# Adding my lambda function to the package
cd ..
zip -g sms-sender-dependencies.zip lambda_function.py

# Redeploying the function
aws lambda update-function-code --function-name book-tid-sms-service --zip-file fileb://sms-sender-dependencies.zip --region eu-north-1