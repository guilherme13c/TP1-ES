import React, { useState } from 'react';

function Login() {
    const [formData, setFormData] = useState({username: "", password: ""});

    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    const handleSubmit = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();

                console.log(data);
            } else {
                throw new Error("login API request failed.")
            }
        } catch (error) {
            console.log(error);
        }
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
