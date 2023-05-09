import React from "react";

function Navbar() {
  return (
    <nav className="navbar">
      <ul>
        <li className="right">
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

