import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReactDOM from "react-dom";
import React from "react";

import './App.css';
import Register from "./pages/register";
import Login from "./pages/login";
import Home from "./pages/home";
import OfferRide from "./pages/offer_ride";
import Rides from "./pages/rides";
import Profile from "./pages/profile";
import MyRides from "./pages/my_rides";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/login/" element={<Login />}/>
        <Route path="/register/" element={<Register />}/>
        <Route path="/offer_ride/" element={<OfferRide />} />
        <Route path="/rides/" element={<Rides />}/>
        <Route path="/profile/" element={<Profile />} />
        <Route path="/my_rides/" element={<MyRides/>} />
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
