import React, { Component } from 'react';
import request from 'superagent'
import Constants from "./Constants"

class Details extends Component {
    constructor(props) {
        super(props);
        this.state = {
            documentId: props.match.params.documentId,
            page: parseInt(props.match.params.page, 10),
            all_pages: 0,
            content: ""
        }
    }

    componentDidMount() {
        let what = ["documents", this.state.documentId, this.state.page].join("/")
        const req = request.get(`${Constants.BASE_URL}${what}`);
        req.end((err, res) => {
            if (err || !res.ok) {
                console.log("Error", err.message);
                this.setState({content: res.body.details.content})
            } else {
                this.setState({content: res.body.details.content, all_pages: res.body.details.pages})
            }
        });
    }


    render() {
        return (
            <div>
                <br />
                <div className='nav-buttons'>
                    { this.state.page > 1 && <a href={"/details/" + this.state.documentId + "/" + (this.state.page-1)} className='btn btn-primary'>Prev</a> }
                    { this.state.page < this.state.all_pages && <a href={"/details/" + this.state.documentId + "/" + (this.state.page+1)} className='btn btn-primary'>Next</a> }
                </div>
                <br />
                <div className='details'>
                    <h1>Page: {this.state.page}</h1>
                    <p>{this.state.content}</p>
                </div>
            </div>
        );
    }
}

export default Details;
