import React, { useContext } from 'react';
import { Redirect, Route } from 'react-router-dom';

import { AuthContext } from '../../context/auth_context.js';

const PrivateRoute = ({ component: Component, ...kwargs }) => {
    const { auth } = useContext(AuthContext);

    return (
        <Route
            {...kwargs}
            render={(props) =>
                auth._id !== undefined ? (
                    <Component {...props} />
                ) : (
                    <Redirect
                        to={{
                            pathname: '/login',
                            state: { from: props.location },
                        }}
                    />
                )
            }
        />
    );
};

export default PrivateRoute;
