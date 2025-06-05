import React from 'react';
import Navbar from '../components/Navbar/Navbar';
import CategoryScrollBar from '../components/CategoryScrollBar/CategoryScrollBar';
import { getCSRFToken, checkAuthenticatedStatus } from '../utils';
import DisplayAllGigs from '../components/DisplayAllGigs';
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from 'react';


const BrowseGigs = () => {
  const navigate = useNavigate()
  
  // Redirect to the login page if not authenticated/logged in
  const checkRedirect= async ()=>{
    const isAuthenticated = await checkAuthenticatedStatus()
    if (isAuthenticated === false){
      navigate("/login")
    }
  }
  useEffect( () => { checkRedirect() }, []);


  return (
    <>
    <Navbar/>
    <CategoryScrollBar/>
    <DisplayAllGigs/>
    </>
  )
}

export default BrowseGigs