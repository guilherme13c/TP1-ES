import React from "react";

export default function DayWrapper(props) {
    const days = ["S", "T", "Q", "Q", "S"];
    
    if (!props.days) {
        return <h1>Error</h1>
    }

    const dayStyles = props.days.map((day, index) => {
        return <div key={index} className={ day ? 'green' : 'red'}>{days[index]}</div>
    });

    return <>{dayStyles}</>;
}