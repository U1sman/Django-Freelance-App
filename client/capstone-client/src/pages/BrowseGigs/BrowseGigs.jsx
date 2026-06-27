import React from 'react';
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from 'react';

import Navbar from '../../components/Navbar/Navbar';
import CategoryScrollBar from '../../components/CategoryScrollBar/CategoryScrollBar';
import { getCSRFToken} from '../../utils';
import { checkAuthenticatedStatus } from '../../apis';
import DisplayAllGigs from '../../components/DisplayAllGigs/DisplayAllGigs';

const BrowseGigs = () => {
  const navigate = useNavigate()
  
  useEffect( () => {
    const redirectLoginpage= async ()=>{
      const response = await checkAuthenticatedStatus();
      const isAuthenticated = response["isAuthenticated"];
      if (!isAuthenticated){
        return navigate("/login");
      };
    };

    redirectLoginpage();
  }, []);


  return (
    <>
    <Navbar/>
    <CategoryScrollBar/>
    <DisplayAllGigs/>
    </>
  )
}

export default BrowseGigs