import React, { useState } from 'react';
import FormWrapper from '../components/FormWrapper';

function Register() {
    const [formData, setFormData] = useState({email: "", person_name: "", gender: "", course: "", neighbourhood: "", password: "", passwordConfirm: ""});

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    const handleSubmit = async (event) => {
        console.log(JSON.stringify(formData))
        if (formData.password !== formData.passwordConfirm) {
            alert("A senha difere da confirmação!")
            return
        }
        if (formData.password.length < 8) {
            alert("A senha deve ter pelo menos 8 caracteres")
            return
        }

        event.preventDefault();

        try {
            const response = await fetch("http://127.0.0.1:8080/register", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();

                console.log(data);
                localStorage.setItem('access_token', data.access_token)
                window.location.href = '/add_ride'
            } else {
                throw new Error("register API request failed.")
            }
        } catch (error) {
            console.log(error);
        }
    }


    return (
        <FormWrapper>
            <form onSubmit={handleSubmit}>
                <label>Nome:
                    <input name='person_name' type='text' onChange={handleChange} value={formData.person_name}/>
                </label>
                <label>Email:
                    <input name='email' type='text' onChange={handleChange} value={formData.email}/>
                </label>
                <label>Sexo:
                    <div onChange={handleChange}>
                        <label>Masculino
                            <input name='gender' type='radio' value='M' id='Male'/>
                        </label>
                        <label>Feminino
                            <input name='gender' type='radio' value='F' id='Female'/>
                        </label>
                    </div>
                </label>
                <label>Curso:
                    <input name='course' type='text' onChange={handleChange} value={formData.course}/>
                </label>
                <label>Bairro:
                    <input name='neighbourhood' type='text' onChange={handleChange} value={formData.neighbourhood}/>
                </label>
                <label>Senha:
                    <input name='password' type='password' onChange={handleChange} value={formData.password}/>
                </label>
                <label>Confirme a senha:
                    <input name='passwordConfirm' type='password' onChange={handleChange} value={formData.passwordConfirm}/>
                </label>
                <button type='submit'>Registrar</button>
            </form>
            <p>Já possui um conta? <a href='/login'>Entre!</a></p>
        </FormWrapper>
    );
}

export default Register;
