import React, { Component } from 'react';

import './App.css'
import axios from 'axios';

import { CSVLink } from "react-csv";
import CsvDownload from "react-json-to-csv";

// <CSVLink
// data={this.state.rowData}
// filename="data.csv"
// // className="hidden"
// // ref={this.csvLink}
// target="_blank">
// Download 
// </CSVLink>


// https://programmingwithmosh.com/javascript/react-file-upload-proper-server-side-nodejs-easy/

class App extends Component {
    constructor(props) {
        super(props);
          this.state = {
            selectedFile: null,
            selectedCompetitorFile: null,
            headers: [],
            data:[] 
          }
       
      }

    onChangeHandler=event=>{
        this.setState({
         selectedFile: event.target.files,
        })
    }

    onChangeCompetitorHandler=event=>{
        this.setState({
         selectedCompetitorFile: event.target.files,
        })
    }

    onClickHandler = () => {
        const data = new FormData()
        for(var x = 0; x<this.state.selectedFile.length; x++) {
            data.append('file', this.state.selectedFile[x])
        }
        for(var x = 0; x<this.state.selectedCompetitorFile.length; x++) {
            data.append('competitor-file', this.state.selectedCompetitorFile[x])
        }
     
       axios.post("http://127.0.0.1:5000/api/upload", data, {
           // receive two    parameter endpoint url ,form data
       })


    .then(res => { // then print response status
        this.setState({ headers: JSON.stringify(res.data.columns) })
        this.setState({ data: JSON.stringify(res.data.rowData,["Keyword"]) })
        // this.setState({ data: JSON.stringify(res.data.rowData,["Keyword"]) })
        // this.setState({ result: JSON.stringify(res.data.rowData) })

        console.log(res.data.columns)
        console.log(res.data.rowData)
        console.log(JSON.stringify(res.data.rows))
        console.log(JSON.stringify(res.data.rowData))
        // console.log(res.data.rowData.Keyword)

         //console.log(typeof res.data);
         //document.getElementById('label').textContent = "Preview";
        document.getElementById('jsonResult').value = JSON.stringify(res.data, undefined, 4);
      })
     
     }

    render() {
        return(
            <div className="container">
                <div className="row">
                <div className="col-md-6">
                    <form method="post" action="#" id="#">
                        <div className="form-group files">
                            <label>Upload Your File </label>
                            <input 
                                type="file" 
                                name="file" 
                                // Show .xls, .xlsx, .csv files...
                                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                                onChange={this.onChangeHandler} 
                                className="form-control" 
                                multiple
                            />
                        </div>

                        <div className="form-group competitor-files">
                            <label>Upload Competitor File </label>
                            <input 
                                type="file" 
                                name="competitor-file" 
                                // Show .xls, .xlsx, .csv files...
                                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                                onChange={this.onChangeCompetitorHandler} 
                                className="form-control" 
                                multiple
                            />
                        </div>
                        <button type="button" className="btn btn-success btn-block" onClick={this.onClickHandler}>Upload</button> 
                    </form>                    
                </div>
                </div>
                <CsvDownload data={this.state.data}>Json to CSV</CsvDownload>

                <CSVLink
                    // headers={this.state.headers}
                    data={this.state.data}
                    filename="data.csv"
                    // className="hidden"
                    // ref={this.csvLink}
                    target="_blank">
                Download 
                </CSVLink>
                <div className="row">
                <div className="col-md-6"><textarea id="jsonResult"></textarea>
                </div>
                </div>
            </div>
        )
    }
}
export default App;