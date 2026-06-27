import React from 'react'
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

import { fetchGig } from '../../apis';
import PaymentSelection from '../../components/PaymentSelection/PaymentSelection';
import PriceSummaryBoxCheckout from '../../components/PriceSummaryBoxes/PriceSummaryBoxCheckout/PriceSummaryBoxCheckout';


const Checkout = () => {
  const navigate= useNavigate()
  const location= useLocation()
  const params = useParams();
  
  const [gig, setGig] = useState({});
  const [requirementsText, setRequirementsText] = useState(null);
  const [pricingOption, setPricingOption] = useState(null);

  useEffect(() => {
    if (!location.state?.requirements || !location.state?.pricingOption) {
      navigate("/");
    } else {
      setRequirementsText(location.state.requirements);
      setPricingOption(location.state.pricingOption);
    }
  }, [location.state, navigate]);

  useEffect( () => { 
      const fetchData = async ()=>{
          const data = await fetchGig(params.gig_id);
          setGig(data);
      }
      fetchData();
      
  }, [params.gig_id]);

  return (
    <>
    <PaymentSelection/>
    <PriceSummaryBoxCheckout gig={gig} pricingOption={pricingOption} requirements={requirementsText} />
    </>
  )
}

export default Checkout