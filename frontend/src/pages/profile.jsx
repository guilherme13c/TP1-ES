import React, { useState } from 'react';
import "../profile.css";
import Navbar from '../components/NavBar';

function Profile() {
    const [formData, setFormData] = useState({email: "", name: "", gender: "", course: "", neighbourhood: "", password: "", passwordConfirm: ""});

    async function getUser(){
        const token = localStorage.getItem('access_token');
        const email = localStorage.getItem('email');

        const response = await fetch("http://127.0.0.1:8080/get_user", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({email: email})
        });

        if (response.ok) {
            const data = await response.json();
            console.log(JSON.stringify(data));
            setFormData(data);
        } else {
            throw new Error("register API request failed.")
        }
    }
    if(formData.email==="") getUser();

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch("http://127.0.0.1:8080/edit_user", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const data = await response.json();
                console.log(JSON.stringify(data));
                alert("Informações atualizadas.")
            } else {
                throw new Error("register API request failed.")
            }
        } catch (error) {
            console.log(error);
        }
    }

    const handleUserDelete = async (event) => {
        event.preventDefault();

        try {
            const token = localStorage.getItem('access_token');
            const userEmail = localStorage.getItem('email');

            const response = await fetch("http://127.0.0.1:8080/delete_user", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({email: userEmail})
            });

            console.log(JSON.stringify(response));

            if (response.ok) {
                window.location.href = '/';
            }
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div className='profile-page'>
            <Navbar/>
            <div className='prof'>
                <div className='left'>
                    <h2>Seu perfil</h2>
                    <img src={require("../default.jpg")} className='profile_pic' alt='profile-pic'/>
                    <button onClick={() => window.location.href="/my_rides"} className="button">Gerenciar caronas</button>
                    <button onClick={() => window.location.href="/offer_ride"} className="button">Oferecer carona</button>
                </div>
                <div className='form'>
                    <form onSubmit={handleSubmit}>
                        <label><span>Nome</span>
                            <input name='name' type='text' onChange={handleChange} value={formData.name}/>
                        </label>
                        <label><span>Sexo</span>
                            <div onChange={handleChange}>
                                <label className="check">
                                    <input name='gender' type='radio' value='M' id='Male' checked={formData.gender==='M'}/>
                                    <span>Masculino</span>
                                </label>
                                <label className="check">
                                    <input name='gender' type='radio' value='F' id='Female' checked={formData.gender==='F'}/>
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
                        <button className='delete-button' onClick={handleUserDelete}>Apagar conta</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Profile;
