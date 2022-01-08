import React, { Component, Fragment } from 'react';
import '../form.css';
// import 'bootstrap/dist/css/bootstrap.css'
import { Button, Form } from 'react-bootstrap'
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
                {/* <form onSubmit={this.handleSubmit} id='searchListingsForm'>
                    <h1>Enter Some Details...</h1>
                        
                    <div className='form-group cnt-field'>
                        <label htmlFor="inputEmail"> Neighbourhood </label> 
                        <select> /* to-do use neighbourhoodOptions *
                            <option value="nb1">nb1</option>
                            <option value="nb2">nb2</option>
                            <option defaultValue="nb3">nb3</option>
                            <option value="nb4">nb4</option>
                        </select>
                    </div>

                    <button className="formSubmitButton">
                        Submit
                    </button>
                </form> */}

                <Form >
                    <h1 className="form-title">Find your Airbnb!</h1>
                    <Form.Group className="mb-3">
                        <Form.Label>Neighbourhood</Form.Label>
                        <Form.Select>
                            <option>Neighbourhood 1</option>
                            <option>Neighbourhood 2</option>
                            <option>Neighbourhood 3</option>
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Preferred Amenities</Form.Label>
                        <Form.Check type="checkbox" label="amn1" />
                        <Form.Check type="checkbox" label="amn2" />
                        <Form.Check type="checkbox" label="amn3" />
                    </Form.Group>
                    <Button variant="light" className="submitButton" type="submit">Submit</Button>
                </Form>

                {/* <ButtonGroup>
                    {radios.map((radio, idx) => (
                    <ToggleButton
                        key={idx}
                        id={`radio-${idx}`}
                        type="radio"
                        variant={idx % 2 ? 'outline-success' : 'outline-danger'}
                        name="radio"
                        value={radio.value}
                        checked={radioValue === radio.value}
                        onChange={(e) => setRadioValue(e.currentTarget.value)}
                    >
                        {radio.name}
                    </ToggleButton>
                    ))}
                </ButtonGroup> */}


                </div>

            </Fragment>
        );
    }
}
 
export default SearchListings;