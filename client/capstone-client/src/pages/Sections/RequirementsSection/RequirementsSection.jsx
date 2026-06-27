import React from 'react'

const RequirementsSection = ({order}) => {
    if (!order) return null;

  return (
    <>
    <h2>Requirements that you provided to the seller</h2>
    <p>{order.requirements}</p> 
    </>
  )
}

export default RequirementsSection