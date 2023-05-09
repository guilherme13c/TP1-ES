import React, { useEffect, useState } from "react";
import RideTable from "../components/RideTable";
import Navbar from "../components/NavBar";

function Rides() {
    const [rides, setRides] = useState([]);

    useEffect(() => {
        async function fetchRides() {
            const token = localStorage.getItem('access_token');

            const response = await fetch("http://127.0.0.1:8080/get_rides", {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const json = await response.json();
            console.log(json['rides'])
            setRides(json['rides']);
        }
        fetchRides();
        console.log("data:", rides)
    }, []);


    return (
        <div className="rides-page">
            <Navbar/>
            {RideTable(rides)}
            <hr />
            <button onClick={() => {window.location.href="/offer_ride"}} className="create-ride">Criar uma nova carona</button>
        </div>
    );
}

export default Rides;