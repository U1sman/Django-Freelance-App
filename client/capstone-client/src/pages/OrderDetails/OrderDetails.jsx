import React from 'react'
import MiniGigBox from '../../components/miniGigBox/miniGigBox';
import PriceSummaryBox from '../../components/PriceSummaryBox/PriceSummaryBox';
import { useParams } from 'react-router-dom';
import { fetchGig } from '../../utils';
import { useState, useEffect } from 'react';

const OrderDetails = () => {
  const params = useParams();
  const [gig, setGig] = useState({});

  useEffect( () => { 
      const fetchData = async ()=>{
          const data = await fetchGig(Number(params.gig_id));
          setGig(data);
      }
      fetchData();
      
  }, [Number(params.gig_id)]);

  return (
    <>
    <MiniGigBox gig={gig} />
    <PriceSummaryBox gig={gig} pricingOptionId={Number(params.pricingOptionId)} />

    </>
  )
}

export default OrderDetails