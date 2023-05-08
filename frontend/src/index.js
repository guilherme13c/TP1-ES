import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReactDOM from "react-dom";
import React from "react";

import Register from "./pages/register";
import Login from "./pages/login";
import Home from "./pages/home";
import './App.css';
import OfferRide from "./pages/offer_ride";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/login/" element={<Login />}/>
        <Route path="/register/" element={<Register />}/>
        <Route path="/offer_ride/" element={<OfferRide />}/>
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
