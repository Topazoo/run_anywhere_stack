import React, { useContext } from 'react';
import { Redirect, Route } from 'react-router-dom';

import { AuthContext } from '../../context/auth_context.js';

const AdminRoute = ({ component: Component, ...kwargs }) => {
    const { auth } = useContext(AuthContext);

    return (
        <Route
            {...kwargs}
            render={(props) =>
                auth.permissions && auth.permissions.includes('ADMIN') ? (
                    <Component {...props} />
                ) : (
                    <Redirect
                        to={{
                            pathname: '/',
                            state: { from: props.location },
                        }}
                    />
                )
            }
        />
    );
};

export default AdminRoute;
