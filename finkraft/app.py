# -*- coding: utf-8 -*-
"""
Created on Mon May  6 18:55:53 2024

@author: sarve
"""

#import mysqldb

from getpass import getpass
from mysql.connector import connect, Error

   
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename

#---------------- File Upload------------------------
 
UPLOAD_FOLDER = 'staticFiles/uploads'

df = pd.DataFrame()
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
 
app = Flask(__name__)
 
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
app.secret_key = 'This is your secret key to utilize session in Flask'
 
 
@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
 
        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)
 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
                           
 
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
        
        return render_template('index2.html')
    return render_template("index.html")
 
    
#---------------------File Upload Complete---------------------- 
 
@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    df = uploaded_df
    print(uploaded_df)
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html',
                           data_var=uploaded_df_html)


#--------------------Uploaded File in Dataframe--------------------

from sqlalchemy import create_engine
engine = create_engine('mysql+mysqldb://root:sarkar02@localhost/testdb')

#DataFrame.to_sql(name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None)

@app.route('/send_data')
def sendData():
    df.to_sql('transaction', con=engine, if_exists='append', index=False)
    result_df = pd.read_sql('transaction', con=engine)
    print(result_df)

    
 
 
if __name__ == '__main__':
    app.run(debug=False)
    


