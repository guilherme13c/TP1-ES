import React, { useState } from 'react';
import FormWrapper from '../components/FormWrapper';

function Login() {
    const [formData, setFormData] = useState({username: "", password: ""});

    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    const handleSubmit = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch("http://127.0.0.1:8080/login", {
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
        <FormWrapper>
            <form onSubmit={handleSubmit}>
                <label><span>Usuário</span>
                    <input type='text' name='username' value={formData.username} onChange={handleChange}/>
                </label>
                <label><span>Senha</span>
                    <input type='password' name='password' value={formData.password} onChange={handleChange}/>
                </label>
                <button type='submit'>Login</button>
            </form>
            <p className="small">Ainda não possui conta? <a href="/register">Cadastre-se</a></p>
        </FormWrapper>
    );
}

export default Login;
