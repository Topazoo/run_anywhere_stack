import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import * as _ from 'lodash';
import React, { useContext, useEffect, useMemo, useState } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import Header from './components/Header';
import Home from './components/Home';
import Navbar from './components/Navbar.js';
import Footer from './components/Footer';
import LoginSignup from './components/LoginSignup';
// import PasswordResetForm from './components/forms/password_reset_form.js';
// import FourOhFour from './components/fourohfour.js';
import PrivateRoute from './components/routes/private_route.js';

import { AuthContext } from './context/auth_context.js';
import {
    refreshTokenManager,
    revokedTokenManager,
} from './context/auth_utils.js';
import './index.css';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.REACT_APP_API_URL;

// Ensure we only set the interceptors once
let axiosReqInterceptor = null;
let axiosRespInterceptor = null;

function App() {
    const { auth, authDispatch } = useContext(AuthContext);

    const debouncedTokenManager = useMemo(
        () => _.debounce(() => refreshTokenManager(auth, authDispatch), 5000),
        [auth, authDispatch],
    );

    useEffect(() => {
        // Attach interceptor to get refresh token if necessary
        if (!!axiosReqInterceptor || axiosReqInterceptor === 0) {
            axios.interceptors.request.eject(axiosReqInterceptor);
        }
        axiosReqInterceptor = axios.interceptors.request.use(
            async (config) => {
                debouncedTokenManager();
                return config;
            },
            (error) => Promise.reject(error),
        );

        // Attach interceptor to detect token refresh failures in API responses
        if (!!axiosRespInterceptor || axiosRespInterceptor === 0) {
            axios.interceptors.response.eject(axiosRespInterceptor);
        }
        axiosRespInterceptor = axios.interceptors.response.use(
            (config) => config,
            (error) => revokedTokenManager(auth, authDispatch, error),
        );
    }, [auth, authDispatch, debouncedTokenManager]);

    // TODO - Add components
    return (
        <div className="app">
            <Header></Header>
            <Navbar></Navbar>
            <Switch>
                <Route exact path="/login" component={LoginSignup} />
                <PrivateRoute exact path="/home" component={Home} />
                <Redirect exact path="/" to="/home" />
                <Redirect to="/404" />
            </Switch>
            <Footer></Footer> 
        </div>
    );
}

export default App;
