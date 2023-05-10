import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/NavBar";
import DayWrapper from "../components/DayWrapper";

function Ride() {
    const { ride_id } = useParams();
    const userEmail = localStorage.getItem('email');

    const [rideData, setRideData] = useState({ days:[false,false,false,false,false], orig: "", dest: "", time: "", mon: false, tue: false, wed: false, thu: false, fri: false, seats_offered: 0, driver_id: ""});
    
    useEffect(() => {
        async function fetchRide() {
            const token = localStorage.getItem('access_token');

            const response = await fetch("http://127.0.0.1:8080/get_ride", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({"ride_id": `${ride_id}`})
            });

            const json = await response.json();
            console.log(JSON.stringify(json));
            setRideData(json);
        }
        fetchRide();
        console.log("rideData: ", rideData);
    }, []);

    const handleRideDelete = async () => {
        const token = localStorage.getItem('access_token');

        const response = await fetch("http://127.0.0.1:8080/delete_ride", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({"ride_id": `${ride_id}`})
        });

        const json = await response.json();
        console.log(JSON.stringify(json));

        if (response.ok) {
            window.location.href = '/rides';
        }
    }

    return (
        <div className="ride-page">
            <Navbar />
            <div className="wrapper">
                <div className="prof">
                    <div className='form'>
                        <label><span>Origem</span>
                            <input name='orig' type='text' value={rideData.orig} disabled/>
                        </label>
                        <label><span>Destino</span>
                            <input name='dest' type='text' value={rideData.dest} disabled/>
                        </label>
                        <label><span>Horário</span>
                            <input name='time' type='text' value={rideData.time} disabled/>
                        </label>
                        <label><span>Assentos disponíveis</span>
                            <input name='seats_offered' type='text' value={rideData.seats_offered} disabled/>
                        </label>
                        <div className="label"><span>Dias</span>
                            <label className="check">
                                <input name='mon' type='checkbox' checked={rideData.days[0]} onClick={function(){return false;}}/>
                                <span>Segunda-feira</span>
                            </label>
                            <label className="check">
                                <input name='tue' type='checkbox' checked={rideData.days[1]} onClick={function(){return false;}}/>
                                <span>Terça-feira</span>
                            </label>
                            <label className="check">
                                <input name='wed' type='checkbox' checked={rideData.days[2]} onClick={function(){return false;}}/>
                                <span>Quarta-feira</span>
                            </label>
                            <label className="check">
                                <input name='thu' type='checkbox' checked={rideData.days[3]} onClick={function(){return false;}}/>
                                <span>Quinta-feira</span>
                            </label>
                            <label className="check">
                                <input name='fri' type='checkbox' checked={rideData.days[4]} onClick={function(){return false;}}/>
                                <span>Sexta-feira</span>
                            </label>
                        </div>
                        <button className="delete-ride button" onClick={handleRideDelete}>Deletar</button>
                    </div>
                    {/* <ul>
                        <li>Origem: {rideData.orig}</li>
                        <li>Destino: {rideData.dest}</li>
                        <li>Horário: {rideData.time}</li>
                        <li>Assentos disponíveis: {rideData.seats_offered}</li>
                        <li><DayWrapper days={rideData.days}/></li>
                        <li><button className="delete-ride" onClick={handleRideDelete}>Deletar</button></li>
                    </ul> */}
                </div>
            </div>
        </div>
    );

    // if (rideData.driver_id === userEmail) {
    //     return (
    //         <div className="rides-page">
    //             <Navbar />
    //             <div>
    //                 <ul>
    //                     <li>Origem: {rideData.orig}</li>
    //                     <li>Destino: {rideData.dest}</li>
    //                     <li>Horário: {rideData.time}</li>
    //                     <li>Assentos disponíveis: {rideData.seats_offered}</li>
    //                     <li><DayWrapper days={rideData.days}/></li>
    //                     <li><button className="delete-ride" onClick={handleRideDelete}>Deletar</button></li>
    //                 </ul>
    //             </div>
    //         </div>
    //     );
    // } else {
    //     return (
    //         <div className="rides-page">
    //             <Navbar />
    //             <div>
    //                 <ul>
    //                     <li>Origem: {rideData.orig}</li>
    //                     <li>Destino: {rideData.dest}</li>
    //                     <li>Horário: {rideData.time}</li>
    //                     <li>Assentos disponíveis: {rideData.seats_offered}</li>
    //                     <li className="day_wrapper"><DayWrapper days={rideData.days}/></li>
    //                 </ul>
    //             </div>
    //         </div>
    //     );
    // }
}

export default Ride;