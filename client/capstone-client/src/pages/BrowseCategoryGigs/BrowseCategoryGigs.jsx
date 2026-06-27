import React from 'react'
import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

import Navbar from '../../components/Navbar/Navbar';
import CategoryScrollBar from '../../components/CategoryScrollBar/CategoryScrollBar';
import { checkAuthenticatedStatus } from '../../apis';

const BrowseCategoryGigs = () => {
  const params = useParams();
  const navigate = useNavigate();
  const [categoryGigs, setCategoryGigs] = useState([]);

  useEffect( () => {
    const redirectLoginpage= async ()=>{
      const response = await checkAuthenticatedStatus();
      const isAuthenticated = response["isAuthenticated"];
      if (!isAuthenticated){
        return navigate("/login");
      };
    };

    const fetchAllCategoryGigs = async () =>{
      let response = await fetch( `http://127.0.0.1:8000/api/get_categoryGigs/${params.categoryName}/`, {
      method: 'GET',
      });
      let result = await response.json();
      setCategoryGigs(result)
    };

    redirectLoginpage();
    fetchAllCategoryGigs();

  }, []);
  return (
    <>

    <Navbar/>
    <CategoryScrollBar/>
    
    <div className="gigsContainer">
    {categoryGigs.map((gig) => {
        return (
        <div className="gigCard" key={gig.id}>
            <Link to={`/gig/${gig.id}`}>{gig.title}</Link>
        </div>
        );
    })}
    </div>

    </>
  )
}

export default BrowseCategoryGigs