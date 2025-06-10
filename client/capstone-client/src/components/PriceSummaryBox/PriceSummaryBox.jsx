import React from 'react'

const PriceSummaryBox = ({gig, pricingOptionId}) => {
  
  const pricingOption = gig?.pricing_plan?.pricing_options.find(pricing_option => pricing_option.id === pricingOptionId)
  console.log(pricingOption)

    
  return (
    <>
    <p>order type: </p>
    </>
  )
}

export default PriceSummaryBox