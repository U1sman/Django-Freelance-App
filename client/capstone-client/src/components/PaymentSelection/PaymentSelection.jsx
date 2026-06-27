import React, { useState } from 'react'
import styles from './PaymentSelection.module.scss'
import { useRef } from 'react'

const PaymentSelection = () => {
    const [selectedMethod, setSelectedMethod] = useState(null)

  return (
    <>
    <h2>Payment Selection</h2>
    <div className="selectionArea">
        <div className="cardSelection">
            <h3>Credit/Debit Card</h3>
            <input type="radio" onChange={() => setSelectedMethod("card")} checked={selectedMethod === "card"} />
            <div className={`${styles.cardDetails} ${ selectedMethod === "card" ? styles.visible : styles.invisible}`}>
                <p>Card Number</p>
                <input type="password" />
                <p>Security Code</p>
                <input type="password" />
                <p>First Name</p>
                <input type="text" />
                <p>Last Name</p>
                <input type="text" />
            </div>
        </div>
        <div className="paypalSelection" >
            <h3>Paypal</h3>
            <input type="radio" onChange={() => setSelectedMethod("paypal")} checked={selectedMethod === "paypal"} />
            <div className={`${styles.paypalDetails} ${ selectedMethod === "paypal" ? styles.visible : styles.invisible}`}>
                <p>Email</p>
                <input type="email" />
            </div>
        </div>
    </div>
    </>
  )
}

export default PaymentSelection