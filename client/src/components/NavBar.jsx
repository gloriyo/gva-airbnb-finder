import React, { Component, Fragment } from 'react';
import { Container, Navbar, Nav } from 'react-bootstrap'

class NavBar extends Component {
    render() { 
        return (
            <Fragment>
                <Navbar bg="light" variant="light">
                <Container>
                    <Navbar.Brand href="/">Welcome</Navbar.Brand>
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            <Nav.Link href="/SearchListings">Search</Nav.Link>
                            <Nav.Link href="#">Feature 1</Nav.Link>
                            <Nav.Link href="#">Feature 2</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>

                </Container>
            </Navbar>
            </Fragment>
        );
    }
}
 
export default NavBar;