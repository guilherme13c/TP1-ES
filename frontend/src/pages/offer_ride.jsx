import React, { useState } from 'react';
import FormWrapper from '../components/FormWrapper';

function OfferRide() {
    const [formData, setFormData] = useState({orig: "", dest: "", time: "", mon: false, tue: false, wed: false, thu:false, fri:false, seats_offered:0});

    function handleChange(event) {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: value}));
    }

    function handleCheck(event) {
        const { name } = event.target;
        setFormData((prevFormData) => ({...prevFormData, [name]: !prevFormData[name]}));
    }

    const handleSubmit = async(event) => {
        event.preventDefault();

        try {
            let fd2={...formData};
            fd2.days=[formData.mon,formData.tue,formData.wed,formData.thu,formData.fri];
            delete fd2.mon;
            delete fd2.tue;
            delete fd2.wed;
            delete fd2.thu;
            delete fd2.fri;
            
            const token = localStorage.getItem('access_token');

            fd2.seats_offered=+fd2.seats_offered;
            fd2.driver_id=0;
            const response = await fetch("http://127.0.0.1:8080/add_ride", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(fd2)
            });

            if (response.ok) {
                const data = await response.json();

                console.log(data)
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
                <label><span>Origem</span>
                    <input type='text' name='orig' value={formData.orig} onChange={handleChange}/>
                </label>
                <label><span>Destino</span>
                    <input type='text' name='dest' value={formData.dest} onChange={handleChange}/>
                </label>
                <label><span>Horário</span>
                    <input type='text' name='time' value={formData.time} onChange={handleChange}/>
                </label>
                <label><span>Assentos</span>
                    <input type='number' name='seats_offered' value={formData.seats_offered} onChange={handleChange}/>
                </label>
                <div className="label"><span>Dias</span>
                    <label className="check"><span>Segunda-feira</span>
                        <input name='mon' type='checkbox' value={formData.mon} onChange={handleCheck}/>
                    </label>
                    <label className="check"><span>Terça-feira</span>
                        <input name='tue' type='checkbox' value={formData.tue} onChange={handleCheck}/>
                    </label>
                    <label className="check"><span>Quarta-feira</span>
                        <input name='wed' type='checkbox' value={formData.wed} onChange={handleCheck}/>
                    </label>
                    <label className="check"><span>Quinta-feira</span>
                        <input name='thu' type='checkbox' value={formData.thu} onChange={handleCheck}/>
                    </label>
                    <label className="check"><span>Sexta-feira</span>
                        <input name='fri' type='checkbox' value={formData.fri} onChange={handleCheck}/>
                    </label>
                </div>
                <button type='submit'>Criar carona</button>
            </form>
        </FormWrapper>
    );
}

export default OfferRide;
