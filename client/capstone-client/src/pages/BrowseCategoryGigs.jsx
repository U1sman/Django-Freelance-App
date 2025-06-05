import React from 'react'
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import Navbar from '../components/Navbar/Navbar';
import CategoryScrollBar from '../components/CategoryScrollBar/CategoryScrollBar';

const BrowseCategoryGigs = () => {
  const params = useParams();
  const [categoryGigs, setCategoryGigs] = useState([]);

  const fetchAllCategoryGigs = async () =>{
      let response = await fetch( `http://127.0.0.1:8000/api/get_categoryGigs/${params.categoryName}/`, {
      method: 'GET',
      });
      let result = await response.json();
      setCategoryGigs(result)
  };

  useEffect( () => { fetchAllCategoryGigs() }, [params.categoryName]);
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