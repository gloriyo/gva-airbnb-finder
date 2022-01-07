import React, { Component, Fragment } from 'react';
import '../form.css';

import Home from './Home'

class SearchListings extends Home {


    constructor(props){
        super(props);
        this.state = {
            inputs: {
                Neighbourhood: '',
                AmenityPriorityByType: [],
                AmenitiesByName: [],
            },
            maxAmenitiesLength: 50,
            errors: {}
        }
        
    }

    // Fetch the list on first mount
    // componentDidMount() {
    //     this.getList();
    // }
    
    // // Retrieves the list of items from the Express app
    // getList = () => {
    //     fetch('/api/list', {
    //         headers : { 
    //           'Content-Type': 'application/json',
    //           'Accept': 'application/json'
    //         }
    //     })
    //     .then(res => res.json())
    //     .then(list => this.setState({ list }))
    //     console.log('calling express api')
    // }
    renderMaxLength (keyName) {
        let maxStringLength = '50';
        return maxStringLength;
    }

    renderError (keyName) {
        if (this.state.errors[keyName]) {
          return <p className='formError'>{this.state.errors[keyName]}</p>;
        }
    }


    render() { 
        // const { inputs } = this.state;
        const { Neighbourhood, AmenityPriorityByType, AmenitiesByName } = this.state.inputs;
        return (
            <Fragment>
                <form onSubmit='/api/getListings' id='searchListingsForm'>
                    <h1>Enter Some Details...</h1>
                        {Object.keys(input).map((keyName, i) => (
                        <div key="inputDiv_{{i}}" className='inputDiv'>
                            <label>{keyName}</label>
                            {this.renderError(keyName)}
                            <textarea
                                className='serachInputs'
                                name={keyName}
                                type='text'
                                value={input[keyName]}
                                onChange='#'
                                maxLength={this.maxAmenitiesLength}
                            >
                            </textarea>
                        </div>
                        ))
                    }
                    <button className="formSubmitButton">
                        Submit
                    </button>
                </form>

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
 
export default SearchListings;