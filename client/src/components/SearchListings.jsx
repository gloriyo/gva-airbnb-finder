import React, { Component, Fragment } from 'react';
import '../form.css';

import Home from './Home'

class SearchListings extends Home {


    constructor(props){
        super(props);
        this.state = {
            neighbourhoodOptions : [],
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
    componentDidMount() {
        this.getNeighbourhoods();
    }
    
    // Retrieves the list from the Express app
    getNeighbourhoods = () => {
        fetch('/api/getNeighbourhoods', {
            headers : { 
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            }
        })
        .then(res => res.json())
        .then(neighbourhoodOptions => this.setState({ neighbourhoodOptions }))
        console.log('calling express api')
    }
    renderMaxLength (keyName) {
        let maxStringLength = '50';
        return maxStringLength;
    }

    renderError (keyName) {
        if (this.state.errors[keyName]) {
          return <p className='formError'>{this.state.errors[keyName]}</p>;
        }
    }

    handleSubmit = async e => {
        e.preventDefault();
        console.log("submitting form")
        alert('submit form')
        // to-do call /api/getListings
    }
    

    render() { 
        // const { inputs } = this.state;
        const { Neighbourhood, AmenityPriorityByType, AmenitiesByName } = this.state.inputs;
        const Neighbourhoods = this.state.neighbourhoodOptions
        return (
            <Fragment>
                <div className='cnt-form'>
                <form onSubmit={this.handleSubmit} id='searchListingsForm'>
                    <h1>Enter Some Details...</h1>
                        {/* {Object.keys(inputs).map((keyName, i) => (
                        <div key="inputDiv_{{i}}" className='inputDiv'>
                            <label>{keyName}</label>
                            {this.renderError(keyName)}
                            <textarea
                                className='serachInputs'
                                name={keyName}
                                type='text'
                                value={inputs[keyName]}
                                onChange='#'
                                maxLength={this.maxAmenitiesLength}
                            >
                            </textarea>
                        </div>
                        ))} */}
                        
                        <label htmlFor="#"> Neighbourhood </label> 
                        <select> {/* to-do use neighbourhoodOptions */}
                            <option value="nb1">nb1</option>
                            <option value="nb2">nb2</option>
                            <option defaultValue="nb3">nb3</option>
                            <option value="nb4">nb4</option>
                        </select>
                    <button className="formSubmitButton">
                        Submit
                    </button>
                </form>
                </div>

            </Fragment>
        );
    }
}
 
export default SearchListings;