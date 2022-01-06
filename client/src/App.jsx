import React, { Component } from 'react';
import { Outlet, Route, Routes, Navigate } from "react-router-dom";

import { Container } from 'react-bootstrap'


import NavBar from "./components/NavBar";

import './App.css';

export default function App() {
  // constructor() {
  //   super();
  //   this.state = {
  //       pageHeader: "Home"
  //   };

  //   this.updatePageHeader = this.updatePageHeader.bind(this);
  //   console.log("constructed")
  // }

  // componentDidMount() {
  //   console.log("mounted")
  // }

  // componentDidUpdate() {
  //   this.setState((state, props) => ({
  //     pageHeader: props.pageHeader
  //   }));
  // }

	const [data, setData] = React.useState(null);

	React.useEffect(() => {
    fetch("/api")
    	.then((res) => res.json())
    	.then((data) => setData(data.message));
	}, []);

  
    console.log("rendering") 
    return (
      <div>
        <NavBar />
        <div>
			<Outlet />

        </div>
      </div>
    );
}

