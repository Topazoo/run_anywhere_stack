import React from 'react';

const LinearLoader = ({ show, children }) =>
    show ? (
        <div className="linear-loader">
            <div className="linear-loader__bar" />
        </div>
    ) : (
        <>{children}</>
    );

export default LinearLoader;
