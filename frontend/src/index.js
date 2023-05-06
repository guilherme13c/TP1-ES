import { BrowserRouter, Routes, Route } from "react-router-dom";
import ReactDOM from "react-dom";
import React from "react";

import Register from "./pages/register";
import Login from "./pages/login";
import Home from "./pages/home";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/login/" element={<Login />}/>
        <Route path="/register/" element={<Register />}/>
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
