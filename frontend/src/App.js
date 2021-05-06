import React, { Component } from 'react';

import './App.css'
import axios from 'axios';

// https://programmingwithmosh.com/javascript/react-file-upload-proper-server-side-nodejs-easy/

class App extends Component {
    constructor(props) {
        super(props);
          this.state = {
            selectedFile: null
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
         console.log(res.data);
         //console.log(typeof res.data);
         //document.getElementById('label').textContent = "Preview";
         document.getElementById('jsonResult').value = JSON.stringify(res.data, undefined, 4);
      })
    //   .then(response => response.json())
    //   .then(data => console.log(data));
     
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
                <div className="row">
                <div className="col-md-6"><textarea id="jsonResult"></textarea>
                </div>
                </div>
            </div>
        )
    }
}
export default App;