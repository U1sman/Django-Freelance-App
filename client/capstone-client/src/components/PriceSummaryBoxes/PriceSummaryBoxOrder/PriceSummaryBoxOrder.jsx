import React from 'react'

const PriceSummaryBoxOrder = ({gig, order}) => {
    const pricingOption = gig?.pricing_plan?.pricing_options.find(pricing_option => pricing_option.id === order?.related_pricing_option);
    
  return (
    <>
    <img src={`http://127.0.0.1:8000${gig?.cover_image}`} alt="cover_image" />
    <p>Ordered From: {gig?.related_seller?.username}</p>
    <p>Package Type: {pricingOption?.type}</p>
    <p>Total: {pricingOption?.price}</p>
    <p>Delivery Time: {pricingOption?.delivery_time} days</p>
    <p>Order ID: {order?.id}</p>
    </>
  )
}

export default PriceSummaryBoxOrder