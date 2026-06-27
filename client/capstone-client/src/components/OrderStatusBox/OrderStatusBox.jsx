import React from 'react'
import styles from './OrderStatusBox.module.scss'
import { format, isValid } from 'date-fns';

import { formatDateTime } from '../../utils';

const OrderStatusBox = ({order}) => {
  if (!order) return null;

  const formattedOrderedDate = formatDateTime(order.created_on);
  const formattedDeliveryDate = formatDateTime(order.delivery_date);


  return (
    <div className={styles.orderStatusBox}>
        <p>Order Status: {order?.status}</p>
        <p>Order Placed On: {formattedOrderedDate}</p>
        <p>Delivery Date: {formattedDeliveryDate}</p>
    </div>
  )
}

export default OrderStatusBox