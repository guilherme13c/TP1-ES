import React, { useState } from 'react';
import FormWrapper from '../components/FormWrapper';

function Login() {
    const [formData, setFormData] = useState({ email: "", password: "" });

    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    const handleSubmit = async(event) => {
        event.preventDefault();

        try {
            console.log(JSON.stringify(formData))
            const response = await fetch("http://127.0.0.1:8080/login", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();

                console.log(JSON.stringify(data));
                localStorage.setItem('access_token', data.access_token)
                window.location.href = '/offer_ride'
                localStorage.setItem('email', data.email)
            } else {
                throw new Error("login API request failed.")
            }
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <FormWrapper>
            <form onSubmit={handleSubmit}>
                <label><span>Usuário</span>
                    <input type='text' name='email' value={formData.email} onChange={handleChange}/>
                </label>
                <label><span>Senha</span>
                    <input type='password' name='password' value={formData.password} onChange={handleChange}/>
                </label>
                <button type='submit'>Entrar</button>
            </form>
            <p className="small">Ainda não possui conta? <a href="/register">Cadastre-se</a></p>
        </FormWrapper>
    );
}

export default Login;
