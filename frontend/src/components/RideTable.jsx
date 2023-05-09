import React from "react";


function DayWrapper(props) {
  const days = ["S", "T", "Q", "Q", "S"];

  const dayStyles = props.days.map((day, index) => {
    return <div key={index} style={{backgroundColor: day ? 'green' : 'red'}}>{days[index]}</div>
  });

  return <div>{dayStyles}</div>;
}

function RideTableRow(ride) {
    const navigateToRide = () => window.location.href = `/ride/${ride.ride_id}`;

    return (
        <tr onClick={navigateToRide} className="ride-table-row">
            <td>Origem: {ride.orig}</td>
            <td>Destino: {ride.dest}</td>
            <td>Horário: {ride.time}</td>
            <td><DayWrapper days={ ride.days }/></td>
            <td>Assentos disponíveis: {ride.seats_offered}</td>
        </tr>
    )
}

function RideTable(rides) {
    if (!rides || !rides.length) {
        return (
            <div className="empty-table">
                <h2 className="empty-table-message">Não há caronas disponíveis.</h2>
            </div>
        );
    }

    return (
        <table className="rides-table">
            <tbody>
                {rides && rides.map(ride => RideTableRow(ride))}
            </tbody>
        </table>
    );
}

export default RideTable;