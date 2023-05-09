import React, { useEffect, useState } from "react";
import RideTable from "../components/RideTable";
import Navbar from "../components/NavBar";

function MyRides() {
    const [myRides, setMyRides] = useState([]);

    useEffect(() => { 
        async function fetchMyRides() {
            const token = localStorage.getItem('access_token');
            const userEmail = localStorage.getItem('email');

            const response = await fetch("http://127.0.0.1:8080/get_my_rides", {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const json = await response.json();
            console.log(json["myRides"]);
            setMyRides(json['myRides'])
        }
        fetchMyRides()
        console.log("myRides: ", myRides)
    }, []);

    return (
        <div className="my-rides-page">
            <Navbar />
            <h2 className="title">Minhas Corridas</h2>
            {RideTable(myRides)}
            <hr />
            <button onClick={() => {window.location.href="/offer_ride"}} className="create-ride">Criar uma nova carona</button>
        </div>
    );
}
