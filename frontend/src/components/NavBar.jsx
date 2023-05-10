import React from "react";

function Navbar() {
  return (
    <nav className="navbar">
      <ul>
        <li>
          <h2>FaculRide</h2>
        </li>
        <li className="right">
          <a href="/">Home</a>
        </li>
        <li className="left">
          <a href="/rides">Caronas</a>
        </li>
        <li className="left">
          <a href="/profile">Perfil</a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;

