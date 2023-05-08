import React, { useEffect, useState } from "react";
import RideTable from "../components/RideTable";

function Rides() {
    const [data, setData] = useState([]);

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
            setData(json);
        }
        fetchRides();
    }, []);

    return (
        <div className="rides-page">
            {RideTable(data)}
        </div>
    );
}

export default Rides;