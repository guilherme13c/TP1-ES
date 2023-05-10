import React from "react";
import DayWrapper from "./DayWrapper";

function RideTableRow(ride) {
    const navigateToRide = () => window.location.href = `/ride/${ride.ride_id}`;

    return (
        <div onClick={navigateToRide} className="ride-table-row">
            <div><strong>Origem:</strong> {ride.orig}</div>
            <div><strong>Destino:</strong> {ride.dest}</div>
            <div><strong>Horário:</strong> {ride.time}</div>
            <div><strong>Assentos disponíveis:</strong> {ride.seats_offered}</div>
            <div className="day_wrapper"><DayWrapper days={ ride.days }/></div>
        </div>
    )
}

function RideTable(rides) {
    if (!rides || !rides.length) {
        return (
            <div className="empty-table">
                <p className="empty-table-message">Não há caronas disponíveis.</p>
            </div>
        );
    }

    return (
        <div className="rides-table">
            {/* <tbody> */}
                {rides && rides.map(ride => RideTableRow(ride))}
            {/* </tbody> */}
        </div>
    );
}

export default RideTable;