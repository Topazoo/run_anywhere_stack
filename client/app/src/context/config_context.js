import React, { createContext, useReducer } from 'react';

export const ConfigContext = createContext();

const initialState = [];

const configReducer = (state, action) => {
    Object.freeze(state);
    let newState = Object.assign({}, state);
    switch (action.type) {
        case 'RECEIVE_CONFIGS':
            for (const config in action.configs.data) {
                newState[action.configs.data[config]._id] =
                    action.configs.data[config];
            }
            return newState;
        case 'ADD_CONFIG':
            newState[action.config.data._id] = JSON.parse(
                action.config.config.data,
            );
            return newState;
        case 'UPDATE_CONFIG':
            newState[action.config._id] = {
                ...newState[action.config._id],
                ...action.config,
            };
            return newState;
        case 'REMOVE_CONFIG':
            delete newState[action.config?._id];
            return newState;
        default:
            return state;
    }
};

export const ConfigsContextProvider = (props) => {
    const [configs, dispatch] = useReducer(configReducer, initialState);

    return (
        <ConfigContext.Provider value={{ configs, configsDispatch: dispatch }}>
            {props.children}
        </ConfigContext.Provider>
    );
};
