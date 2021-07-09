import flask
import json
import requests
import sqlite3
import logging
import helper
from flask import request, jsonify, Response
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS, cross_origin

# Logging All Information in a File name app.log
logging.basicConfig(
    filename='app.log',
    filemode='a+',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')
logging.info('\n\n\nServer Restarted\n')

# Initiating Flask App
app = flask.Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger6.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL,
                                              API_URL,
                                              config={'app_name': "Xmeme_API"})
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# Handling CORS Requests
CORS(app)

# Setting DEBUG Value
app.config["DEBUG"] = True
# app.config.from_envvar('APP_SETTINGS')

# Global variable for faster fetching of data
res = []
ult = 0

# Database Path
db_path = 'xmeme.db'


# Route ('/memes') for GET and POST Method


@app.route('/memes', methods=['GET', 'POST'])
@cross_origin()
def apiMain():
    global res, ult

    # Handling Post request
    if request.method == 'POST':
        logging.info('Handling Post Request')
        status_code = 500
        id = None
        try:
            # Connecting to Database
            conn = sqlite3.connect(db_path)

            # extracting Params from Json
            name, caption, url, status_code = helper.extract_json_param(
                request, 0)

            # Checking if JSON paramaters were correct
            if status_code == 400:
                raise Exception('Bad request, Incorrect paramaters')

            # Checking url content type
            if not helper.checkUrl(url):
                status_code = 406

            else:
                status_code = 500
                c = conn.cursor()
                ##inserting in database
                c.execute(
                    "INSERT into memes (name, caption, url) values (?,?,?)",
                    (name, caption, url))

                # Inserting in Global List too
                if ult == 1:
                    res.insert(
                        0, {
                            "id": f"{(len(res) + 1)}",
                            "name": name,
                            "caption": caption,
                            "url": url
                        })

                logging.info('Successful Insertion of the Post')

                if ult == 1:
                    id = len(res)
                else:
                    command = f"SELECT rowid FROM memes WHERE url = '{url}'"
                    c1 = conn.cursor()
                    c1.execute(command)
                    id = c1.fetchone()
                # Successfully Inserted Meme
                status_code = 201
        except sqlite3.IntegrityError:
            # If Unique constrain of URL is Violated
            status_code = 409
            conn.rollback()
            logging.exception('Exception in Post Request')
            id = None
        except Exception:
            # Other Internal Errors
            conn.rollback()
            logging.exception('Exception in Post Request')
            id = None
        finally:
            conn.commit()
            conn.close()
            # Closing the database
            if id:
                res_post = jsonify({"id": str(id)})
            else:
                res_post = jsonify({})
            return res_post, status_code

    else:
        # Handling Get Request
        logging.info('Handling Get Request')
        status_code = None
        if ult == 0:
            res, status_code = helper.get_all()
            ult = 1
            if status_code == 200:
                return jsonify(res), 200
            else:
                return jsonify({}), status_code
        else:
            return jsonify(res), 200


# Route ('/memes/<id>') for GET and PATCH Methods
@app.route('/memes/<id>', methods=['GET', 'PATCH'])
@cross_origin()
def apiId(id):
    global res, ult
    try:
        id = int(id)
    except:
        return "Bad Id request", 400
    if request.method == 'PATCH':
        # Handling Patch request
        logging.info('Handling Patch Request')
        status_code = 500
        try:
            conn = sqlite3.connect(db_path)
            caption, url, status_code = helper.extract_json_param(
                request, 1)

            # Checking if JSON paramaters were correct
            if status_code == 400:
                raise Exception('Bad request, Incorrect paramaters')

            c = conn.cursor()
            status_code = 500

            # Check if Id is available or not
            command = f"SELECT rowid,* FROM memes WHERE rowid = {id}"
            c.execute(command)
            row = c.fetchone()

            # If result is NUll, raiseException
            if str(row) == "None":
                raise NameError("No Meme with this Id")

            # Updating in Database if only caption is there
            if caption and (not url):
                c.execute("UPDATE memes SET caption = ? WHERE rowid = ?",
                          (caption, id))
                if ult == 1:
                    res[len(res) - id]['caption'] = caption

            # Check if Url is available already in database
            elif (url):
                command = f"SELECT rowid FROM memes WHERE url = '{url}'"
                c.execute(command)
                row = c.fetchone()

                # If result is NUll, raiseException
                if str(row) != "None":
                    raise sqlite3.IntegrityError("unique constraint error")

                # Checking of Url Content-type
                if not helper.checkUrl(url):
                    status_code = 406
                    raise Exception('Url is not image')

                #Updating in Database
                if caption and url:
                    c.execute(
                        "UPDATE memes SET caption = ?, url = ? WHERE rowid = ?",
                        (caption, url, id))

                    # Updating Global List if exist
                    if ult == 1:
                        res[len(res) - id]['caption'] = caption
                        res[len(res) - id]['url'] = url
                else:
                    c.execute("UPDATE memes SET url = ? WHERE rowid = ?",
                              (url, id))

                    # Updating Global List if exist
                    if ult == 1:
                        res[len(res) - id]['url'] = url

            logging.info('Successful handling')
            status_code = 204
        except sqlite3.IntegrityError:
            # If Unique constrain of URL is Violated
            status_code = 409
            conn.rollback()
            logging.exception('Exception in Patch Request')
        except NameError:
            # Meme with particular Id is not Present
            logging.exception('No meme with this Id')
            status_code = 404
        except Exception:
            # Other Internal Errors
            conn.rollback()
            logging.exception('Exception in Patch Request')
        finally:
            # Closing Database
            conn.commit()
            conn.close()
            return jsonify(None), status_code
    else:
        # Handling request for a particular meme id
        logging.info('Handling Get Request for a Particular Id')
        status_code = 500
        ans = None
        try:
            # Connecting with Database

            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            command = f"SELECT rowid,* FROM memes WHERE rowid = {id}"
            c.execute(command)
            row = c.fetchone()

            # If result is NUll, raiseException
            if str(row) == "None":
                raise NameError("No Meme with this Id")
            ans = jsonify({
                "id": f"{row[0]}",
                "name": f"{row[1]}",
                "caption": f"{row[2]}",
                "url": f"{row[3]}"
            })
            status_code = 200

            # Succesfully executed this request
            logging.info('Successful handling')
        except NameError:
            # Meme with particular Id is not Present
            logging.exception('No meme with this Id')
            status_code = 404
            ans = jsonify({"msg": "No Meme with this Id"})

        except Exception:
            # Other internal Exceptions
            logging.exception('Exception while Get Meme with Id')
            status_code = 500
            ans = jsonify({"msg": "Internal server error"})

        finally:
            # Closing Database
            conn.rollback()
            conn.close()
            return ans, status_code


# Error 404 Page


@app.errorhandler(404)
@cross_origin()
def page_not_found(e):
    return jsonify("Url Not found"), 404


if __name__ == "__main__":
    app.run(port=8081)
