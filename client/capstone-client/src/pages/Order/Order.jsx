import React from 'react'
import { useState, useEffect } from 'react'
import { Link, useNavigate, useParams, useLocation } from 'react-router-dom'
import { format, isValid } from 'date-fns';

import { checkAuthenticatedStatus, fetchGig, fetchOrder } from '../../apis';
import PriceSummaryBoxOrder from '../../components/PriceSummaryBoxes/PriceSummaryBoxOrder/PriceSummaryBoxOrder';
import OrderStatusBox from '../../components/OrderStatusBox/OrderStatusBox';
import DetailsSection from '../Sections/DetailsSection/DetailsSection';
import RequirementsSection from '../Sections/RequirementsSection/RequirementsSection';
import DeliverySection from '../Sections/DeliverySection/DeliverySection';

const Order = () => {
  const params = useParams();
  const [order, setOrder] = useState(null)
  const [gig, setGig] = useState(null)
  const location = useLocation();
  const navigate = useNavigate();
  // if the path is the default order/order_id path without a trailing hash then a trailing hash "#details" is added
  const currentSection = location.hash || "#details";

  useEffect( () => { 
    const initializePage = async ()=>{
      const response = await checkAuthenticatedStatus();
      const isAuthenticated = response["isAuthenticated"];
      const currentUser = response["currentUser"];

      if (!isAuthenticated){
        return navigate("/login");
      }

      const orderData = await fetchOrder(params.order_id);

      if (!orderData) return; // Wait until order is fetched
      if (currentUser?.id !== orderData?.buyer){
        return navigate("/");
      }  

      setOrder(orderData);

      const gigData = await fetchGig(orderData.related_gig);
      setGig(gigData);

      
    };

    initializePage();

  }, [params.order_id]);


  // useEffect( () => {
  //   const checkAcess= async ()=>{
      
  //     const response = await checkAuthenticatedStatus();
  //     const isAuthenticated = response["isAuthenticated"];
  //     const currentUser = response["currentUser"];

  //     if (!isAuthenticated){
  //       return navigate("/login");
  //     }

  //     if (!order) return; // Wait until order is fetched
  //     if (currentUser?.id !== order?.buyer?.id){
  //       navigate("/");
  //     }

  //   };

  //   checkAcess();

  // }, [order]);


  useEffect(() => {
    if (!location.hash) {
      navigate(`${location.pathname}#details`, { replace: true });
    }
  }, [location, navigate]);


  return (
    <>
    {currentSection === "#details" && <DetailsSection order={order} gig={gig} />}
    {currentSection === "#requirements" && <RequirementsSection order={order} />}
    {currentSection === "#delivery" && <DeliverySection order={order} />}

    <PriceSummaryBoxOrder gig={gig} order={order}/>
    <OrderStatusBox order={order} />

    </>
  )
}

export default Order