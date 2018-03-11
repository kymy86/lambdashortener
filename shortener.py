from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import random
import boto3
import os
import botocore

app = Flask(__name__)
CORS(app)

s3 = boto3.client('s3')
_S3_BUCKET = os.getenv('BUCKET_NAME')
_S3_URL = os.getenv('BUCKET_URL')

def is_valid_url(url):
    # Checking URL validity...
    regex = re.compile(
        r'^(?:http)s?://' #http/https
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url)

def _random_url(new_url):
    # Generate the random code for the url shortener
    whitelist = 'abcdefghijklmnopqrstuvwxyzABCDEFGIJKLMNOPQRSTUVWXYZ0123456789'
    new_url += whitelist[random.randrange(0, len(whitelist))]
    if len(new_url) < 8:
        return _random_url(new_url)
    else:
        if _is_code_exist(new_url):
            new_url = ""
            return _random_url(new_url)
        else:
            return new_url

def _is_code_exist(code):
    #check if the object with this code already exists in S3
    try:
        response = s3.head_object(Bucket=_S3_BUCKET,Key=code)
        return True
    except botocore.exceptions.ClientError:
        return False

def _create_s3_object(code, url):
    #generate the s3 object with the redirection in place
    s3.put_object(
        Key=code,
        Bucket=_S3_BUCKET,
        WebsiteRedirectLocation=url
    )
    return _S3_URL+"/"+code
    

def generate_short_url(url):

    gen_url = ""
    if len(gen_url) < 8:
        gen_url = _random_url(gen_url)

    s3_url = _create_s3_object(gen_url, url)
    return s3_url

@app.route('/', methods=['POST'])
def lambda_handler():

    url = request.json.get('url')
    if not url:
        return jsonify({'error':'Please provide an URL '}), 400
    if not is_valid_url(url):
        return jsonify({'error':'Please, provide a valid URL'}), 400

    short_url = generate_short_url(url)
    
    return jsonify({'shorturl':short_url}), 200


if __name__ == '__main__':
    app.run(debug=True)