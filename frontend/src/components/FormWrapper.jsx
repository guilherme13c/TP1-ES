import React from 'react';

function FormWrapper({children}) {
    return (
        <div className="wrapper">
            <div className="form">
                {children}
            </div>
        </div>
    );
}

export default FormWrapper;
