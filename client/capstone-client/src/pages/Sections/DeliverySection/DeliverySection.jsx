import React from 'react'
import { useEffect, useState } from 'react';

import { fetchAllOrderDeliveries } from '../../../apis'
import { formatDateTime } from '../../../utils';

const DeliverySection = ({order}) => {
  if (!order) return null;
  const [allDeliveries, SetAllDeliveries]= useState([]);

  useEffect( () => {
    const fetchData = async ()=>{
      const deliveries = await fetchAllOrderDeliveries(order?.id);
      SetAllDeliveries(deliveries);
      console.log(deliveries);
    };
    fetchData();
  }, [order?.id]);

  return (
    <>
    {allDeliveries.map((delivery)=>{
      return(
        <div className="deliveryContainer" key={delivery.id}>
          <div className="delivery">
            <p>You received a delivery from {delivery.sender.username}</p>
            <p>{delivery.message}</p>
            <p>status: {delivery.status}</p>
            <p>received on: {formatDateTime(delivery.created_at)}</p>
            <h3>ATTACHMENTS</h3>
            <div className="deliveryAttachments">
              {delivery.attachments.map((attachment)=>{
                return(
                <a 
                  href={`http://127.0.0.1:8000${attachment?.file_url}`}
                  download
                >Download File #{attachment.id}</a>
                );
              })}
            </div>

          </div>

          <div className="approvalBox">
            <p>
              You received your delivery from deliverySender. <br />
              Satisfied? Please approve the delivery or request revision.
            </p>
            <button className="approveDelivery">I Approve</button>
            <button className="requestRevision">Request Revision</button>
          </div>
        </div>
      );
    })}
    </>
  )
}

export default DeliverySection