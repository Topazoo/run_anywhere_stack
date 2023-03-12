import React, { createContext, useEffect, useReducer } from 'react';

import { refreshTokenManager } from './auth_utils.js';

export const AuthContext = createContext();

const initialState = JSON.parse(localStorage.getItem('_application_user')) || {};

const authReducer = (state, action) => {
    const id_key = '_application_user';
    Object.freeze(state);
    let newState = Object.assign({}, state);
    switch (action.type) {
        case 'LOGIN':
            localStorage.setItem(id_key, JSON.stringify(action.user));
            return (newState[action.user._id] = action.user);
        case 'REFRESH':
            localStorage.setItem(id_key, JSON.stringify(action.user));
            return (newState[action.user._id] = action.user);
        case 'UPDATE_ATTRS':
            for (const attr in action.user) {
                newState[attr] = action.user[attr];
            }
            localStorage.setItem(id_key, JSON.stringify(action.user));
            return newState;
        case 'LOGOUT':
            newState = {};
            localStorage.removeItem(id_key);
            return newState;
        default:
            return state;
    }
};

export const AuthContextProvider = (props) => {
    const [auth, dispatch] = useReducer(authReducer, initialState);

    useEffect(() => {
        // Check for token expiration after page refresh
        refreshTokenManager(auth, dispatch, { url: null });
    }, []);

    return (
        <AuthContext.Provider value={{ auth, authDispatch: dispatch }}>
            {props.children}
        </AuthContext.Provider>
    );
};
