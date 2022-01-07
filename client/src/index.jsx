import React from 'react';
import { render } from "react-dom";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import 'bootstrap/dist/css/bootstrap.css'
import Home from "./components/Home";
import NotFound from "./components/NotFound";
import ExpressTest from "./components/ExpressTest.jsx";
import SearchListings from "./components/SearchListings.jsx";

render(
  <BrowserRouter> 
    <Routes>
      <Route path="/" exact element={<App />}>
        <Route path="Home" exact element={<Home />} />
        <Route path="SearchListings" element={<SearchListings />} />
        <Route path="Express-Test" element={<ExpressTest />} />
        <Route path="404" element={<NotFound />} />
        {/* <Navigate to="/404" /> */}
        {/* <Route path="*" element={<Navigate replace to="/404" />} /> */}
      </Route>
    </Routes>
  </BrowserRouter>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
