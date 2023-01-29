# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 19:17:55 2022

@author: user
"""

from flask import Flask, render_template, jsonify
import pandas as pd
from six.moves import urllib
import json

from myAPI import * 

app = Flask(__name__)
 
@app.route("/")
def home():
    return 'hello'




if __name__ == '__main__':
    app.run(port=7000)