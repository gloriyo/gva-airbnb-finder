import React, { Component, Fragment } from 'react';


class ExpressTest extends Component {


    constructor(props){
        super(props);
        this.state = {
            list: []
        }
    }
    
    // Fetch the list on first mount
    componentDidMount() {
        this.getList();
    }
    
    // Retrieves the list of items from the Express app
    getList = () => {
        fetch('/api/list', {
            headers : { 
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            }
        })
        .then(res => res.json())
        .then(list => this.setState({ list }))
        console.log('calling express api')
    }

    render() { 
        const { list } = this.state;
        return (
            <Fragment>
                <div class="page-header pb-2 mt-4 mb-2 border-bottom">
                    <h1>Message from Backend Server (express)</h1>
                    <h1>List of Items</h1>
                    {/* Check to see if any items are found*/}
                    {list.length ? (
                    <div>
                        {/* Render the list of items */}
                        {list.map((item) => {
                        return(
                            <div>
                            {item}
                            </div>
                        );
                        })}
                    </div>
                    ) : (
                    <div>
                        <h2>No List Items Found</h2>
                    </div>
                    )
                }
                </div>
            </Fragment>
        );
    }
}
 
export default ExpressTest;