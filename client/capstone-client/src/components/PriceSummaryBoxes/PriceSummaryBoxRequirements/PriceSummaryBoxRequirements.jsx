import React from 'react'
import { Link, useNavigate} from 'react-router-dom'


const PriceSummaryBoxRequirements = ({gig, pricingOptionId, requirements}) => {
  
  const pricingOption = gig?.pricing_plan?.pricing_options.find(pricing_option => pricing_option.id === pricingOptionId)
  const navigate = useNavigate()

  const saveRequirements = ()=>{
    if (requirements.length >= 200 && requirements.length < 3000){ 
      navigate(`/gig/${gig?.id}/checkout`, {state:{pricingOption, requirements}})
    }
    else{
      alert("requirements is length is wrong")
    }
  }

  return (
    <>
    <h3>Price Summary</h3>
    <p>Package Type: {pricingOption?.type}</p>
    <p>Total: {pricingOption?.price}</p>
    <p>Delivery Time: {pricingOption?.delivery_time} days</p>

    <button onClick={saveRequirements}>Continue to Checkout</button>
    </>
  )
}

export default PriceSummaryBoxRequirements