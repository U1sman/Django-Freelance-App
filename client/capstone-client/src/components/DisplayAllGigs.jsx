import React from 'react'
import { getCSRFToken } from '../utils';
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

const DisplayAllGigs = () => {
  const [gigs, setGigs] = useState([]);
  const fetchAllGigs = async () =>{
      let response = await fetch("http://127.0.0.1:8000/api/get_all_gigs/", {
      method: 'GET',
      });
      let result = await response.json();
      setGigs(result)
  };

  useEffect( () => {
    fetchAllGigs()
  }, []);
    
  return (
    <>

      <div className="gigsContainer">
        {gigs.map((gig) => {
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

export default DisplayAllGigs