import React, { useState } from 'react';
import "../profile.css";

function Profile() {
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
                window.location.href = '/offer_ride'
            } else {
                throw new Error("register API request failed.")
            }
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div className='prof'>
            <div className='left'>
                <h2>Seu perfil</h2>
                <img src={require("../default.jpg")} class='profile_pic' />
                <button type='submit' class="button">Gerenciar caronas</button>
                <button type='submit' class="button">Oferecer carona</button>
            </div>
            <div className='form'>
            <form onSubmit={handleSubmit}>
                <label><span>Nome</span>
                    <input name='person_name' type='text' onChange={handleChange} value={formData.person_name}/>
                </label>
                <label><span>Email</span>
                    <input name='email' type='text' onChange={handleChange} value={formData.email}/>
                </label>
                <label><span>Sexo</span>
                    <div onChange={handleChange}>
                        <label className="check">
                            <input name='gender' type='radio' value='M' id='Male'/>
                            <span>Masculino</span>
                        </label>
                        <label className="check">
                            <input name='gender' type='radio' value='F' id='Female'/>
                            <span>Feminino</span>
                        </label>
                    </div>
                </label>
                <label><span>Curso</span>
                    <input name='course' type='text' onChange={handleChange} value={formData.course}/>
                </label>
                <label><span>Bairro</span>
                    <input name='neighbourhood' type='text' onChange={handleChange} value={formData.neighbourhood}/>
                </label>
                <button type='submit'>Alterar</button>
            </form>
            </div>
        </div>
    );
}

export default Profile;
