import React, { useEffect, useState } from "react";
import RideTable from "../components/RideTable";
import Navbar from "../components/NavBar";

// TODO: Fix, not working
function MyRides() {
    const [myRides, setMyRides] = useState([]);

    useEffect(() => { 
        async function fetchMyRides() {
            const token = localStorage.getItem('access_token');
            const userEmail = localStorage.getItem('email');

            const response = await fetch("http://127.0.0.1:8080/get_my_rides", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({email: userEmail})
            });

            const json = await response.json();
            console.log(JSON.stringify(json));
            setMyRides(json['userRides'])
        }
        fetchMyRides()
        console.log("userRides: ", myRides);
    }, []);

    return (
        <div className="rides-outer">
            <Navbar />
            <div className="rides-page">
                <div>
                    <h2 className="title">Minhas Corridas</h2>
                    {RideTable(myRides)}
                    <button onClick={() => {window.location.href="/offer_ride"}} className="create-ride button">Criar uma nova carona</button>
                </div>
            </div>
        </div>
    );
}

export default MyRides;