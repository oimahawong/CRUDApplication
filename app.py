from flask import Flask, redirect, jsonify, request

import logging
import boto3 
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s %(funcName)s():%(lineno)i: - %(levelname)s - %(message)s' )
ch.setFormatter(formatter)
logger.addHandler(ch)


client = boto3.client('s3',region_name='us-west-2')

app = Flask(__name__)

@app.route('/del_fav_foods')
def del_fav_foods():
    logger.debug("here")

    client = boto3.client('s3')
    client.delete_object(Bucket = 'fav-foods-bucket', Key = 'fav_food.txt')
    return jsonify(status = "OK")

@app.route('/read_fav_foods')
def read_fav_foods():
    logger.debug("here")

    client = boto3.client('s3')
    try:
        obj = client.get_object(Bucket = 'fav-foods-bucket', Key = 'fav_food.txt')
    except:
        return jsonify( status = "Error")
    return jsonify(status = "OK", fav_foods= str(obj['Body'].read()) )

@app.route('/create_fav_foods')
def create_fav_foods():
    logger.debug("here")
    logger.debug( "Fav Foods Parm = {request.args.get('fav_foods')}")

    client = boto3.client('s3')
    client.put_object(
    Body=request.args.get('fav_foods'),
    Bucket='fav-foods-bucket',
    Key='fav_foods.txt',
    ContentType='text/plain'
)
 
    return jsonify(status = "OK", fav_foods=request.args.get('fav_foods'))

@app.route('/update_fav_foods')
def update_fav_foods():
    logger.debug("here")
    logger.debug( "Fav Foods Parm = {request.args.get('fav_foods')}")

    client.put_object(
    Body=request.args.get('fav_foods'),
    Bucket='fav-foods-bucket',
    Key='fav_foods.txt',
    ContentType='text/plain'
)
    return jsonify(status = "OK", fav_foods=request.args.get('fav_foods'))

@app.route('/')
def redir_to_static_home():
    return redirect('/static/index.html')

if __name__ == '__main__':
    print("Run Server")
    logger.info("Mad Man's Assignment")
    app.run(host='0.0.0.0')