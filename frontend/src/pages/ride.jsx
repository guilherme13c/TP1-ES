import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/NavBar";
import DayWrapper from "../components/DayWrapper";

function Ride() {
    const { ride_id } = useParams();

    const [rideData, setRideData] = useState({ orig: "", dest: "", time: "", mon: false, tue: false, wed: false, thu: false, fri: false, seats_offered: 0 });
    
    useEffect(() => {
        async function fetchRide() {
            const token = localStorage.getItem('access_token');
            console.log(ride_id)

            const response = await fetch("http://127.0.0.1:8080/get_ride", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({"ride_id": `${ride_id}`})
            });

            const json = await response.json();
            console.log(JSON.stringify(json))
            setRideData(json);
        }
        fetchRide();
        console.log("rideData: ", rideData);
    }, []);

    async function handleRequest() {
        return;
    }

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
                    <li><button className="request-button" onClick={handleRequest}>Pedir para entrar</button></li>
                </ul>
            </div>
        </div>
    );
}

export default Ride;