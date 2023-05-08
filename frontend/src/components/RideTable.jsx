import React from "react";
import { useNavigate } from "react-router-dom";


function RideTableRow(ride) {
    const navigate = useNavigate();
    
    const navigateToRide = () => navigate(`/ride/${ride.ride_id}`);

    return (
        <tr onClick={navigateToRide} className="ride-table-row">
            <td>{ride.orig}</td>
            <td>{ride.dest}</td>
            <td>{ride.time}</td>
            <td>{ride.days}</td>
            <td>{ride.seats_offered}</td>
        </tr>
    )
}

function RideTable(rides) {
    return (
        <table className="rides-table">
            {rides.map(ride => 
                RideTableRow(ride)
            )}
        </table>
    );
}

export default RideTable;