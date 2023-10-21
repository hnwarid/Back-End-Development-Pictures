from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    'return all pictures data requested'
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pict in data:
        if pict['id'] == id:
            return pict
    return {'message': 'picture not found'}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    posted_pict = request.json
    print(posted_pict)
    
    for pict in data:
        if posted_pict['id'] == pict['id']:
            return {'Message': f"picture with id {posted_pict['id']} already present"}, 302
    data.append(posted_pict)
    return posted_pict, 201
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_pict = request.json
    print(updated_pict)

    for i, pict in enumerate(data):
        if updated_pict['id'] == pict['id']:
            data[i] = updated_pict
            return pict, 201
    return {'message': 'picture not found'}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pict in data: 
        if pict['id'] == id:
            data.remove(pict)
            return '', 204
    return {'message': 'picture not found'}, 404
