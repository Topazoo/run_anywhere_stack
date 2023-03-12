import React, {useContext} from 'react';
import { AuthContext } from '../context/auth_context';
import { Link } from 'react-router-dom';
import axios from 'axios';
import '../stylesheets/Navbar.css';

function Navbar() {
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
    <nav className="navbar">
      <ul className="navbar-nav">
        <li className="nav-item">
          <Link to="/" className="nav-link">
            Home
          </Link>
        </li>
        <li className="nav-item">
          <button className="nav-link" onClick={logout}>
            Logout
          </button>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
