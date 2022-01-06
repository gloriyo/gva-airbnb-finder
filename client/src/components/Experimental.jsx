import React, { Component, Fragment } from 'react';
import Card from 'react-bootstrap/Card'


class Listing extends Component {
    render() { 
        return (
            <Fragment>
                <Card style={{ width: '18rem' }}>
                <Card.Img variant="top" src="holder.js/100px180" />
                <Card.Body>
                    <Card.Title>Card Title</Card.Title>
                    <Card.Text>
                    Some quick example text to build on the card title and make up the bulk of
                    the card's content.
                    </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
                </Card.Body>
                </Card>
            </Fragment>
        );
    }
}
 
export default Listing;