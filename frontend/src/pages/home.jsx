import React from 'react';
import { useNavigate } from "react-router-dom";

function Home() {
    const navigate = useNavigate();

    const navigateToLogin = () => {
        navigate("/login");
    }

    const navigateToRegister = () => {
        navigate("/register");
    }

    return (
        <div className='home'>
            <h1 className='title'>Faculride</h1>
            <div className='redirection-buttons'>
                <button className='login-redirect' onClick={navigateToLogin}>Entrar</button>
                <hr/>
                <button className='register-redirect' onClick={navigateToRegister}>Registrar</button>
            </div>
        </div>
    );
}

export default Home;
