import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter } from 'react-router-dom';

import App from './App';
import { AuthContextProvider } from './context/auth_context';
import { UsersContextProvider } from './context/users_context';
import './index.css';

// import reportWebVitals from './reportWebVitals';

ReactDOM.render(
    <HashRouter>
        <UsersContextProvider>
            <AuthContextProvider>
                <App />
            </AuthContextProvider>
        </UsersContextProvider>
    </HashRouter>,
    document.getElementById('root'),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
