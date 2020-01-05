import os
import io
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask import send_from_directory, render_template, session
from werkzeug.utils import secure_filename
from PIL import Image
import random
import time
import json

import pandas as pd
import numpy as np
import uuid
import Queue


# csv_data = pd.read_csv('fakedata.csv') 
# # print(csv_data)
# csv_data_list = csv_data.values.tolist()
# print csv_data_list

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def p1():
    csv_data = pd.read_csv('/home/cayu/Desktop/AIoT-master/IOT/flask_website/fakedata.csv') 
    # print(csv_data)
    csv_data_list = csv_data.values.tolist()
    print csv_data_list
    # return render_template('index.html',data_name='PM2.5')
    return render_template('index.html',status1_1 = csv_data_list[0][1], status1_2 = csv_data_list[0][2],
                                        status1_3 = csv_data_list[0][3], status1_4 = csv_data_list[0][4],
                                        status1_5 = csv_data_list[0][5], status1_6 = csv_data_list[0][6],
                                        status2_1 = csv_data_list[1][1], status2_2 = csv_data_list[1][2],
                                        status2_3 = csv_data_list[1][3], status2_4 = csv_data_list[1][4],
                                        status2_5 = csv_data_list[1][5], status2_6 = csv_data_list[1][6])


@app.route('/new',methods=['GET'])
def getnew():
    csv_data = pd.read_csv('/home/crazyr/catkin_ws/IOT/flask_website/fakedata.csv') 
    # print(csv_data)
    csv_data_list = csv_data.values.tolist()
    fucktest = csv_data_list[0][1]
    print ("fuuuuck!")
    print (fucktest)
    return json.dumps(fucktest)


if __name__ == '__main__':
    
    app.debug = True
    app.run(host='0.0.0.0')
    time.sleep(1)
