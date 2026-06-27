import React from 'react'
import { format, isValid } from 'date-fns';

import MiniGigBox from '../../../components/MiniGigBox/MiniGigBox';

const DetailsSection = ({order, gig}) => {
    if (!order) return null;
    if (!gig) return null;

    const pricingOption = gig?.pricing_plan?.pricing_options.find(pricing_option => pricing_option.id === order?.related_pricing_option);
    const orderedDate = new Date(order.created_on);
    const deliveryDate = new Date(order.delivery_date);

    const formattedOrderedDate = isValid(orderedDate)
    ? format(orderedDate, "MMM d, yyyy 'at' h:mm a") : "Unknown";

    const formattedDeliveryDate = isValid(deliveryDate)
    ? format(deliveryDate, "MMM d, yyyy 'at' h:mm a") : "Unknown";


  return (
    <>
    <div className="conformationSection">
        <h2>Thank You for placing an Order, It is in the works and will be with you soon.</h2>
        <h3>We have notified the seller about your order.</h3>
        <h3>You should receive your delivery by {formattedDeliveryDate}</h3>
    </div>
    <div className="gigDetailsSection">
        <p>Ordered from {gig.related_seller.username} on {formattedOrderedDate}</p>
        <p>Total Price <span>{pricingOption.price}</span></p>
        <MiniGigBox gig={gig} />
    </div>
    </>
  )
}

export default DetailsSection