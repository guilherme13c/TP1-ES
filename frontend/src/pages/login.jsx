import React, { useState } from 'react';

function Login() {
    const [formData, setFormData] = useState({username: "", password: ""});

    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    function handleSubmit(event) {
        event.preventDefault();

        // TODO: Consume login API
    }

    // TODO: style page
    return (
        <form onSubmit={handleSubmit}>
            <label>Usuário
                <input type='text' name='username' value={formData.username} onChange={handleChange}/>
            </label>
            <label>Senha
                <input type='password' name='password' value={formData.password} onChange={handleChange}/>
            </label>
            <button type='submit'>Login</button>
        </form>
    );
}

export default Login;
