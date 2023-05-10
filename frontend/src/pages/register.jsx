import React, { useState } from 'react';
import FormWrapper from '../components/FormWrapper';

function Register() {
    const [formData, setFormData] = useState({email: "", person_name: "", gender: "", course: "", neighbourhood: "", password: "", passwordConfirm: ""});

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    const handleSubmit = async (event) => {
        if (formData.password !== formData.passwordConfirm) {
            alert("A senha difere da confirmação!")
            return
        }
        if (formData.password.length < 8) {
            alert("A senha deve ter pelo menos 8 caracteres")
            return
        }

        event.preventDefault();
        let fd2={...formData};
        delete fd2.passwordConfirm;
        fd2.name=formData.person_name;
        delete fd2.person_name;

        try {
            const response = await fetch("http://127.0.0.1:8080/register", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(fd2)
            });

            if (response.ok) {
                const data = await response.json();

                console.log(data);
                localStorage.setItem('access_token', data.access_token)
                localStorage.setItem('email', data.email)
                window.location.href = '/rides'
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
                <label><span>Nome:</span>
                    <input name='person_name' type='text' onChange={handleChange} value={formData.person_name}/>
                </label>
                <label><span>Email:</span>
                    <input name='email' type='text' onChange={handleChange} value={formData.email}/>
                </label>
                <div className="label" onChange={handleChange}>
                    <span>Sexo</span>
                    <label className="check">
                        <input name='gender' type='radio' value='M' id='Male'/>
                        <span>Masculino</span>
                    </label>
                    <label className="check">
                        <input name='gender' type='radio' value='F' id='Female'/>
                        <span>Feminino</span>
                    </label>
                </div>
                <label><span>Curso:</span>
                    <input name='course' type='text' onChange={handleChange} value={formData.course}/>
                </label>
                <label><span>Bairro:</span>
                    <input name='neighbourhood' type='text' onChange={handleChange} value={formData.neighbourhood}/>
                </label>
                <label><span>Senha:</span>
                    <input name='password' type='password' onChange={handleChange} value={formData.password}/>
                </label>
                <label><span>Confirme a senha:</span>
                    <input name='passwordConfirm' type='password' onChange={handleChange} value={formData.passwordConfirm}/>
                </label>
                <button type='submit'>Registrar</button>
                <p className="small">Já possui uma conta? <a href='/login'>Entre!</a></p>
            </form>
        </FormWrapper>
    );
}

export default Register;
