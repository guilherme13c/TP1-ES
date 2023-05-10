import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/NavBar";
import DayWrapper from "../components/DayWrapper";

function Ride() {
    const { ride_id } = useParams();
    const userEmail = localStorage.getItem('email');

    const [rideData, setRideData] = useState({ orig: "", dest: "", time: "", mon: false, tue: false, wed: false, thu: false, fri: false, seats_offered: 0, driver_id: ""});
    
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


    if (rideData.driver_id === userEmail) {
        return (
            <div className="ride-page">
                <Navbar />
                <div>
                    <ul>
                        <li>Origem: {rideData.orig}</li>
                        <li>Destino: {rideData.dest}</li>
                        <li>Horário: {rideData.time}</li>
                        <li><DayWrapper days={rideData.days}/></li>
                        <li>Assentos disponíveis: {rideData.seats_offered}</li>
                        <li><button className="delete-ride" onClick={handleRideDelete}>Deletar</button></li>
                    </ul>
                </div>
            </div>
        );
    } else {
        return (
            <div className="ride-page">
                <Navbar />
                <div>
                    <ul>
                        <li>Origem: {rideData.orig}</li>
                        <li>Destino: {rideData.dest}</li>
                        <li>Horário: {rideData.time}</li>
                        <li><DayWrapper days={rideData.days}/></li>
                        <li>Assentos disponíveis: {rideData.seats_offered}</li>
                    </ul>
                </div>
            </div>
        );
    }
}

export default Ride;