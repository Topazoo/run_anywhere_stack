import React, { createContext, useReducer } from 'react';

export const UsersContext = createContext();

const initialState = [];

const usersReducer = (state, action) => {
    Object.freeze(state);
    let newState = Object.assign({}, state);
    switch (action.type) {
        case 'RECEIVE_USERS':
            for (const user in action.users) {
                newState[action.users[user]._id] = action.users[user];
            }
            return newState;
        case 'SET_USERS':
            newState = {};
            for (const user in action.users) {
                newState[action.users[user]._id] = action.users[user];
            }
            return newState;
        case 'UPDATE_USER_PERMISSIONS':
            newState[action.user._id]['permissions'] = action.user.permissions;
            return newState;
        case 'UPDATE_USER':
            newState[action.user._id] = {
                ...newState[action.user._id],
                ...action.user,
            };
            return newState;
        case 'REMOVE_USER':
            delete newState[action.user?._id];
            return newState;
        default:
            return state;
    }
};

export const UsersContextProvider = (props) => {
    const [users, dispatch] = useReducer(usersReducer, initialState);

    return (
        <UsersContext.Provider value={{ users, usersDispatch: dispatch }}>
            {props.children}
        </UsersContext.Provider>
    );
};
