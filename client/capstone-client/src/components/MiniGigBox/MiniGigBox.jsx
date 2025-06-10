import React from 'react'
import { useState, useEffect } from 'react';

const MiniGigBox = ({gig}) => {
    
  return (
    <>
    <h2>{gig.title}</h2>
    <img src={`http://127.0.0.1:8000${gig.cover_image}`} alt="cover_image" />
    placeholder for rating (placeholder for number of reviews)
    
    </>
  )
}

export default MiniGigBox