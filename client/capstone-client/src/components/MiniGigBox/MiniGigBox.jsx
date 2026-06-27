import React from 'react'
import { useState, useEffect } from 'react';

const MiniGigBox = ({gig}) => {
  if (!gig) return null;

  return (
    <>
    <img src={`http://127.0.0.1:8000${gig.cover_image}`} alt="cover_image" />
    <p>{gig.title}</p>
    <p>rating with stars placeholder</p>
    <p>(reviews placeholder)</p>

    </>
  )
}

export default MiniGigBox