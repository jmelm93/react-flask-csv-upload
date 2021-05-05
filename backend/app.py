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
        # Grab each file individually from the request
        csv_list = []
        for file in files:
            csv_list.append(pd.read_csv(file))
        
        result = pd.concat(csv_list, axis=0, ignore_index=True)

        result = result.replace({np.nan: None})

        ##### BELOW ENABLES USING ADDITIONAL UPLOADS ######
        ##### NEED TO WRITE LOOP TO SIMPLY RUN THIS FOR HOWEVER MANY ARE UPLOADED ######

        # dataset2 = files[1]
        # df2 = pd.read_csv(dataset2)
        # frames = [df1, df2]
        # result = pd.concat(frames)
        
        row_count = result.shape[0]
        column_count = result.shape[1]
        column_names = result.columns.tolist()
        final_row_data = []
        for index, rows in result.iterrows():
            final_row_data.append(rows.to_dict())
        json_result = {'rows': row_count, 'cols': column_count, 'columns': column_names, 'rowData': final_row_data}
        
        print(result.head(10))
        # result.to_csv('result.csv')
        # print(json_result)
    
        return json.dumps(json_result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


