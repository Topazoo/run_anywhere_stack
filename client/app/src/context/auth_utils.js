/* Utilities for the authorization context manager */
import axios from 'axios';

export const refreshTokenManager = async (auth, authDispatch) => {
    const _MS_PER_MIN = 1000 * 60;

    // Refresh the token if it's this many minutes away from expiring
    const _REFRESH_IF_UNDER_MINS = 3;

    const user = JSON.parse(localStorage.getItem('_application_user')) || {};

    // If the user is authenticated
    if (user && 'session_expires' in user) {
        // Get the number of minutes until the token will expire
        let mins_until_expiration = Math.floor(
            (new Date(user.session_expires) - new Date()) / _MS_PER_MIN,
        );

        console.log(
            '[Auth Debug] Minutes until session refresh attempt: ' +
                Math.floor(
                    (new Date(user.session_expires) - new Date()) / _MS_PER_MIN,
                ).toString(),
        );
        // If the expiration time has elapsed imminent, fire a request to logout
        if (mins_until_expiration < 0) {
            // Attempt a clean logout
            console.log('[Auth Debug] Session Over - Attempting Logout');

            await axios
                .delete('/api/authenticate', { _id: user._id })
                .then(() => {
                    authDispatch({ type: 'LOGOUT', user: { _id: user._id } });

                    console.log('[Auth Debug] Session expired. Signed out!');
                    // If it fails, force it
                })
                .catch((error) => {
                    authDispatch({ type: 'LOGOUT', user: { _id: user._id } });

                    console.log('[Auth Debug] Session expired. Signed out!');
                });
        }

        // If the expiration time is imminent, fire a request to refresh the token
        else if (mins_until_expiration < _REFRESH_IF_UNDER_MINS) {
            console.log('[Auth Debug] Session Expiring - Attempting Refresh');
            // Attempt a token refresh
            await axios
                .put('/api/authenticate')
                .then((response) => {
                    user.session_expires = response.data.session_expires;
                    authDispatch({ type: 'REFRESH', user: user });

                    console.log('[Auth Debug] Refreshed user session');

                    // If it fails, boot the user to login
                })
                .catch((error) => {
                    authDispatch({ type: 'LOGOUT', user: { _id: user._id } });

                    console.log('[Auth Debug] Token refresh error: ' + error);
                });
        }
    } else {
        console.log('[Auth Debug] No Auth cookie found. Signed out!');
        authDispatch({ type: 'LOGOUT', user: { _id: user._id } });
    }
};

export const revokedTokenManager = (auth, authDispatch, error) => {
    // If the error was that the token couldn't be refreshed, boot the user to login
    const user = JSON.parse(localStorage.getItem('_application_user')) || {};
    if (
        error.response &&
        error.response.data &&
        (error.response.data.error === 'Token has been revoked' ||
            error.response.data.error === 'Signature has expired') &&
        error.config.url !== '/api/authenticate'
    ) {
        console.log(
            '[Auth Debug] Got invalid session: ' + error.response.data.error,
        );
        authDispatch({ type: 'LOGOUT', user: { _id: user._id } });
    }

    // TODO - RETRY REQUEST IF NOT TOKEN ISSUE?
    return Promise.reject(error);
};
