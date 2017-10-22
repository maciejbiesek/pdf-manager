import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import PdfList from './PdfList';
import Details from './Details';

class App extends Component {
    render() {
        return (
            <Router>
                <div className="container">
                    <button className="btn btn-primary-outline"><Link to="/">Home</Link></button>

                    <Route exact path="/" component={PdfList} />
                    <Route path="/details/:documentId/:page" component={Details} />
                </div>
            </Router>
        );
    }
}

export default App;
