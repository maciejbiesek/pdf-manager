import React, { Component } from 'react';
import Dropzone from 'react-dropzone'
import request from 'superagent'
import Constants from "./Constants"

class PdfList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            documents: []
        };
    }

    componentDidMount() {
        let what = "documents"
        const req = request.get(`${Constants.BASE_URL}${what}`);
        req.end((err, res) => {
            if (err || !res.ok) {
                console.log("Error", err.message);
            } else {
                this.setState({documents: res.body.documents})
            }
        });
    }


    render() {
        return (
            <div>
                <br />
                <div className='add-button'>
                    <Dropzone className='btn btn-primary'
                              multiple={false}
                              accept={"application/pdf"}
                              onDrop={this.onDrop}>Add new file</Dropzone>
                </div>
                <br />
                { this.state.documents.length > 0 && <div className='documents-list'>
                    <table className='table table-stripped'>
                        <thead>
                            <tr>
                                <th>Id</th>
                                <th>Filename</th>
                                <th>Number of pages</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.documents.map((item, i) =>
                                <tr key={i}>
                                    <td>{item.id}</td>
                                    <td><a href={"details/" + item.id + "/1"}>{item.filename}</a></td>
                                    <td>{item.pages}</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div> }
            </div>
        );
    }

    onDrop = (acceptedFiles, rejectedFiles) => {
        if (rejectedFiles.length === 0) {
            let what = "documents"
            const req = request.post(`${Constants.BASE_URL}${what}`);
            acceptedFiles.forEach(file => {
                req.attach("file", file);
            });
            req.end((err, res) => {
                if (err || !res.ok) {
                    console.log("Error", err.message);
                } else {
                    alert("Succesfully added");
                    let documents = this.state.documents;
                    documents.push(res.body.document);
                    this.setState({documents: documents});
                }
            });
        } else {
            alert("You can upload only PDF files!")
        }
    }
}

export default PdfList;
