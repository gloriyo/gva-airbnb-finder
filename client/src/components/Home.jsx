import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';

class Home extends Component {
    render() { 
        return (
            <Fragment>
                <div class="page-header pb-2 mt-4 mb-2 border-bottom">
                    <h1>HOME</h1>
                    this is home.... test out the express server 
                    <Link to={'/Express-Test'}>
                        <button>

                            Get Message From Server
                        </button>
                    </Link>


                </div>
            </Fragment>
        );
    }
}
 
export default Home;