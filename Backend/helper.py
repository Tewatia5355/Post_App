import flask
import json
import requests
import sqlite3
import logging
import helper
from flask import request, jsonify, Response

# Database Path
db_path = 'xmeme.db'

# Logging of all essential info
logging.basicConfig(
    filename='app.log',
    filemode='a+',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')


# Function to Fetch all the latest 100 Memes and put them in a Global List of *res*
def get_all():
    res = []
    logging.info('Fetching all Memes from Database')

    # Initiating Status_Code for future reference
    status_code = 500

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        # Fetching top 100 memes by last uploading
        c.execute("SELECT rowid,* FROM memes ORDER BY rowid DESC")
        # Selecting Top 100 Memes
        rows = c.fetchmany(100)
        # Appending Them to a List
        for i in range(len(rows)):
            temp = {
                "id": f"{rows[i][0]}",
                "name": f"{rows[i][1]}",
                "caption": f"{rows[i][2]}",
                "url": f"{rows[i][3]}"
            }
            res.append(temp)
        logging.info('Successful fetching of all memes')

        # Everything is Successful
        status_code = 200
    except Exception:
        logging.exception('Error while fetching memes')
        status_code = 500
    finally:
        conn.close()
        return res, status_code


# Function to check whether given URL content-type is Image or not


def checkUrl(url):
    try:
        logging.info('Image Url Checking')
        x = requests.head(url).headers['Content-Type']

        # Checking Content type
        if (x[0:5] == "image"):
            logging.info('Url Content is Image')
            return True
        else:
            logging.warning('The Given req. isn\'t an image')
            return False
    except Exception:
        logging.exception('Unknown Issues in CheckUrl function')
        return False


def extract_json_param(req, req_method):
    if req_method == 0:
        status_code = 400
        try:
            name = req.json['name']
            caption = req.json['caption']
            url = req.json['url']
            status_code = 200
        except Exception:
            name = caption = url = None
        finally:
            return name, caption, url, status_code
    elif req_method == 1:
        status_code = 400
        url, caption = None, None
        empty = 0
        try:
            caption = req.json['caption']
        except:
            empty = 1
            caption = None

        try:
            url = req.json['url']
            status_code = 200
        except:
            url = None
            if empty == 0:
                status_code = 200
            else:
                status_code = 400

        return caption, url, status_code
