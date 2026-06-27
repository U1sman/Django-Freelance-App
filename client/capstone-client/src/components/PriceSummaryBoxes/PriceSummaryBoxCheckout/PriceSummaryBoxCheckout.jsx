import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'

import { getCSRFToken } from '../../../utils'

const PriceSummaryBoxCheckout = ({gig, pricingOption, requirements}) => {
  const navigate= useNavigate();

  const startOrder= async ()=> {

    const orderData = {
      "gig": gig,
      "pricingOption": pricingOption,
      "requirements": requirements,
    }

    let response = await fetch("http://127.0.0.1:8000/api/create_order/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      //data being sent 
      body: JSON.stringify(orderData),
      credentials: 'include',
    })

    const result = await response.json()

    if (response.ok) {
      alert(result["message"])
      navigate(`/order/${result["order_id"]}`)
    }
    else {
      alert(JSON.stringify(result["error"]))
    }
  }  

  return (
    <>
    <img src={`http://127.0.0.1:8000${gig?.cover_image}`} alt="cover_image" />
    <p>{gig?.title}</p>
    <p>Package Type: {pricingOption?.type}</p>
    <p>Total: {pricingOption?.price}</p>
    <p>Delivery Time: {pricingOption?.delivery_time}</p>
    <button className="startOrder" onClick={startOrder}>Start Order</button>


    </>
  )

}

export default PriceSummaryBoxCheckout