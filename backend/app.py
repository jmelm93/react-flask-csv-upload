from flask import Flask, flash, request, redirect, url_for
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
import os
import pandas as pd
import json
import numpy as np

app = Flask(__name__)
CORS(app) #comment this on deployment

@app.route("/")
def serve(path):
    return "Home"

@app.route('/api/upload', methods = ['POST'])
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        files = request.files.getlist("file")
        competitor_files = request.files.getlist("competitor-file")
        
        csv_list = []
        csv_competitor_list = []

        # Read and concatenate the files sent from the frontend
        for file in files:
            csv_list.append(pd.read_csv(file))
        
        result = pd.concat(csv_list, axis=0, ignore_index=True)
        result = result.replace({np.nan: None})
        
        for file in competitor_files:
            csv_competitor_list.append(pd.read_csv(file))      

        competitor_result = pd.concat(csv_competitor_list, axis=0, ignore_index=True)
        competitor_result = competitor_result.replace({np.nan: None})
        
        # Prepare the result to return
        row_count = result.shape[0]
        column_count = result.shape[1]
        column_names = result.columns.tolist()
        final_row_data = []
        for index, rows in result.iterrows():
            final_row_data.append(rows.to_dict())
        json_result = {'rows': row_count, 'cols': column_count, 'columns': column_names, 'rowData': final_row_data}
        
        # print(competitor_result.head(10))
        # result.to_csv('result.csv')
        # print(json_result)

        # we have to return a JSON object as string in order to be pretty-printed in the frontend
        return json.dumps(json_result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


