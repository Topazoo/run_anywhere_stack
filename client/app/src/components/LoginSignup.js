import axios from 'axios';
import React, { useState, useContext } from 'react';
import { Redirect } from 'react-router-dom';
import { AuthContext } from '../context/auth_context';
import '../stylesheets/LoginSignup.css';

const LoginSignup = () => {
  const { auth, authDispatch } = useContext(AuthContext);
  const [isLogin, setIsLogin] = useState(true);
  const [errors, setErrors] = useState({});


  const handleToggle = () => {
    setIsLogin(!isLogin);
  };


  const login = (e) => {
    e.preventDefault();
    setErrors({});

    const formData = new FormData(e.target);
    const userData = Object.fromEntries(formData.entries()); 

    axios
        .post('/api/authenticate', {
            username: userData.username,
            password: userData.password,
        })
        .then((response) => {
            const authResponse = response.data;
            return axios
                .get(`/api/users?_id=${authResponse._id}`)
                .then((response) => {
                    const user = {
                        ...response.data.data[0],
                        ...{
                            session_expires: authResponse.session_expires,
                        },
                        ...{
                            permissions: authResponse.permissions,
                        },
                    };
                    authDispatch({ type: 'LOGIN', user: user });
                });
        })
        .catch(() => {
            setErrors({
                message:
                    'Username or Password is incorrect. Please try again.',
            });
        });
    };

    const signup = (e) => {
        e.preventDefault();
        setErrors({});

        const formData = new FormData(e.target);
        const userData = Object.fromEntries(formData.entries()); 

        axios
            .post('/api/users', {
                first_name: userData.firstName,
                last_name: userData.lastName,
                email_address: userData.email,
                username: userData.username,
                password: userData.password,
            })
            .then((response) => {
                delete userData.password;

                const user = {...response.data, ...userData};
                authDispatch({ type: 'LOGIN', user: user });
            })
            .catch((e) => {
                // TODO -- Constants file for backend error codes?
                const response = e.response;
                if (
                    response.status == 409 &&
                    response.data.error.includes('email')
                ) {
                    setErrors({message: 'This email is already taken'});
                    return;
                }
                if (
                    response.status == 409 &&
                    response.data.error.includes('username')
                ) {
                    setErrors({message: 'This username is already taken'});
                    return;
                }
            });
    };

    return auth._id === undefined ? (
        <div className="login-signup-container">
        <div className="slider">
            <div className={`toggle ${isLogin ? '' : 'active'}`} onClick={handleToggle}>
            <span>Sign Up</span>
            </div>
            <div className={`toggle ${isLogin ? 'active' : ''}`} onClick={handleToggle}>
            <span>Login</span>
            </div>
        </div>
        <div className="form-container">
            <form className={`form ${isLogin ? 'login-form' : 'signup-form'}`} onSubmit={isLogin ? login : signup}>
                {isLogin ? (
                <>
                    <input type="text" name="username" placeholder="Username" />
                    <input type="password" name="password" placeholder="Password" />
                </>
                ) : (
                <>
                    <input type="text" name="firstName" placeholder="First Name" autocomplete="given-name"/>
                    <input type="text" name="lastName" placeholder="Last Name" autocomplete="family-name"/>
                    <input type="text" name="username" placeholder="Username" autocomplete="off"/>
                    <input type="password" name="password" placeholder="Password" autocomplete="new-password"/>
                    <input type="email" name="email" placeholder="Email" autocomplete="email" className='full-grid-row'/>
                </>
                )}
                <button
                    type="submit"
                    className="full-grid-row"
                >
                    {isLogin ? 'Log In' : 'Sign Up'}
                </button>
            </form>
            </div>
        </div>
        ) : (
        <Redirect to={{ pathname: '/home' }} />
    );
}

export default LoginSignup;
