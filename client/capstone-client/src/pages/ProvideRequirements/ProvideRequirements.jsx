import React from 'react'
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';

import { fetchGig } from '../../apis';
import MiniGigBox from '../../components/MiniGigBox/MiniGigBox';
import PriceSummaryBoxRequirements from '../../components/PriceSummaryBoxes/PriceSummaryBoxRequirements/PriceSummaryBoxRequirements';

const ProvideRequirements = () => {
  const params = useParams();
  const [gig, setGig] = useState({});
  const [requirements, setRequirements] = useState("")

  useEffect( () => { 
      const fetchData = async ()=>{
          const data = await fetchGig(params.gig_id);
          setGig(data);
      }
      fetchData();
      
  }, [params.gig_id]);

  return (
    <>
    <MiniGigBox gig={gig} />
    
    <div className="order_requirements">
      <p>What are your Requirements for this Order?</p>
      <textarea maxLength={3000} onChange={(r)=> setRequirements(r.target.value)} value={requirements}></textarea>
      <p>{requirements.length}/3000</p>
    </div>

    <PriceSummaryBoxRequirements gig={gig} pricingOptionId={Number(params.pricingOptionId)} requirements={requirements} />

    </>   
  )
}

export default ProvideRequirements