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

    onClickHandler = () => {
        const data = new FormData()
        for(var x = 0; x<this.state.selectedFile.length; x++) {
            data.append('file', this.state.selectedFile[x])
        }
     
       axios.post("http://127.0.0.1:5000/api/upload", data, { 
           // receive two    parameter endpoint url ,form data
       })
     
     .then(res => { // then print response status
         console.log(res.statusText)
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
                        <button type="button" className="btn btn-success btn-block" onClick={this.onClickHandler}>Upload</button> 
                    </form>                    
                </div>
                </div>
            </div>
        )
    }
}
export default App;