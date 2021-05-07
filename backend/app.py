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
        
        df_client = []
        df_competitors = []

        # Read and concatenate the files sent from the frontend
        for file in files:
            df_client.append(pd.read_csv(file))
        
        client_result = pd.concat(df_client, axis=0, ignore_index=True)
        client_result = client_result.replace({np.nan: None})
        
        for file in competitor_files:
            df_competitors.append(pd.read_csv(file))      

        competitor_result = pd.concat(df_competitors, axis=0, ignore_index=True)
        competitor_result = competitor_result.replace({np.nan: None})

        def position_range(position):
            if position < 11:
                return "1 to 10"
            elif position >= 11 and position <= 20:
                return "11 to 20"
            elif position >= 21 and position <= 30:
                return "11 to 20"
            else:
                return "31+"
            
        def top20(position):
            if position < 21:
                return "TRUE"
            else:
                return "FALSE"
            
        def traffic_exists(traffic):
            if traffic > 0:
                return "TRUE"
            else:
                return "FALSE"

        domain_name = competitor_result['URL'].str.extract('(?<=http://)(.*?)(?=/)|(?<=https://)(.*?)(?=/)')
        domain_name = domain_name[0].fillna(domain_name[1]).fillna(competitor_result['URL'])

        competitor_result.insert(loc = 2, column = "Position_Range", value = competitor_result["Position"].apply(position_range))
        competitor_result.insert(loc = 3, column = "Top20", value = competitor_result["Position"].apply(top20))
        competitor_result.insert(loc = 7, column = "Domain", value = domain_name)
        competitor_result.insert(loc = 11, column = "Traffic_Exists", value = competitor_result["Traffic"].apply(traffic_exists))
        competitor_result.insert(loc = 11, column = "Traffic_Rank", value = competitor_result["Traffic"].rank(ascending = False).astype(int))

        ### BELOW MERGES THE COMPETITOR DATASET w/ CLIENTS AND CLEANS COLUMN NAMES ###

        df_gap = competitor_result.merge(client_result, how="left", left_on=["Keyword"], right_on=["Keyword"])

        select_cols = ["Keyword","Search Volume_x", "Keyword Difficulty_x", "CPC_x","Position_x", "Position_y",  "Top20", "Position_Range","Traffic_x", "Traffic Cost_x", "URL_x","Domain" ,"URL_y" ]
        df_gap = df_gap[select_cols]

        df_gap = df_gap.rename(
            mapper={
                "Keyword": "Keyword",
                "Search Volume_x": "Search_Volume",
                "Keyword Difficulty_x": "KD",
                "CPC_x": "CPC",

                "Position_x": "Position_Comp",
                "Position_y": "Position_Client",
                "Position_Range": "Position_Range_Comp",
                "Traffic_x": "Traffic_Comp",
                "Top20": "Top20_Comp",
                "Traffic Cost_x": "Traffic_Cost_Comp",


                "URL_x": "URL_Comp",
                "Domain": "Domain",
                "URL_y": "URL_Client",


                "clicks_sum": "clicks_sum_gsc",
                "impressions_sum": "impressions_sum_gsc",
                "ctr_mean": "ctr_mean_gsc",
                "position_size": "count_instances_gsc",
                "position_max": "position_max_gsc",
                "position_min": "position_min_gsc",
                "position_mean": "position_mean_gsc",
                "text": "text_crawl",
                "occurrences": "occurrences_crawl"
            }, axis="columns")

        df_gap = df_gap.fillna(value = "Not Ranking")

        # df_gap.to_csv("GAP_Analysis_testing.csv",  index=False)

        # Prepare the result to return
        row_count = df_gap.shape[0]
        column_count = df_gap.shape[1]
        column_names = df_gap.columns.tolist()
        final_row_data = []
        for index, rows in df_gap.iterrows():
            final_row_data.append(rows.to_dict())
        json_result = {'rows': row_count, 'cols': column_count, 'columns': column_names, 'rowData': final_row_data}

        # we have to return a JSON object as string in order to be pretty-printed in the frontend
        return json.dumps(json_result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


