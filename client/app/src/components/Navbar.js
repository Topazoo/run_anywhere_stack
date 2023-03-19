import React, {useContext} from 'react';
import { AuthContext } from '../context/auth_context';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Navbar, Container, Nav } from 'react-bootstrap';
import '../stylesheets/Navbar.css';

const NavigationBar = () => {
    const { auth, authDispatch } = useContext(AuthContext);

    const logout = () => {
        axios
            .delete('/api/authenticate', {
                data: { _id: auth._id },
            })
            .then((response) => {
                authDispatch({ type: 'LOGOUT', user: { _id: auth._id } });
            })
            .catch((errors) => {
                console.log(errors);
                authDispatch({ type: 'LOGOUT', user: { _id: auth._id } });
            });
    };

    return (
        <Navbar bg="dark" variant="dark" expand="lg">
          <Container>
            <Navbar.Brand href="/">Home</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                {auth._id !== undefined &&
                    <Nav.Link onClick={logout}>Logout</Nav.Link>
                }
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
    );
}

export default NavigationBar;
