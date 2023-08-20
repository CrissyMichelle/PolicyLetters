from flask import Flask, session, render_template, redirect, flash, session, url_for, request, jsonify, current_app
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from key import GOOGLE_MAPS_KEY
# from models import db, connect_db, NewSoldier, Soldier
from forms import GetDirectionsForm, CustomFieldParam
import requests
import logging
import sys
import pdb
import os

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kbymaecc:hmiBfUsgWuKYu7elxc_Pt1-etdxWo-Md@bubble.db.elephantsql.com/kbymaecc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = "psst420"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    """Renders homepage with CG and DCSM"""
    return render_template("/home.html")

@app.route("/policies")
def show_policies():
    """Render page with PDF 'reader' and PDFs"""
    
    pdf_files = [file for file in os.listdir('static/pdfs') if file.endswith('.pdf')]
    return render_template("policies.html", pdf_files=pdf_files)

@app.route("/policies/<policy><int:num>")
def show_single_pdf(policy, num):
    """Render a single policy letter based on the policy's name and number"""
    
    pdf_name = f"{policy}{num}.pdf"
    number = f"{num}"

    return render_template("policy.html", pdf_name=pdf_name, number=number)

@app.route("/log")
def show_log():
    """Render page with Lightning Operations Guide"""
    return render_template("log.html")

@app.route("/api/directions")
def get_directions_for_api_call():
    """Use API to get directions"""

    start = request.args.get('origin')
    end = request.args.get('destination')
    mode = request.args.get('mode')

    data = {
        "origin":  start,
        "destination":  end,
        "travelMode":  mode}

    return jsonify(data)

@app.route("/directions", methods=["GET", "POST"])
def show_get_directions():
    """Render HTML page showing google map and form for api call.  Accepts parameters as query strings"""

    start = request.args.get('origin', 'Lyman Gate, HI')
    end = request.args.get('destination', '')
    mode = request.args.get('mode', 'DRIVING')

    form = GetDirectionsForm()
    return render_template("directions.html", origin=start, destination=end, mode=mode, form=form)

