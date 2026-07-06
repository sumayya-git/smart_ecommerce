import React, { useEffect, useState } from "react";
// import OrderProgress from "../components/OrderProgress";

import { useNavigate } from "react-router-dom";

import {
  getMyOrders,
  cancelOrderService,
  requestReturnService,
  downloadInvoiceService,
} from "../services/orderService";

import STATUS from "../constants/orderStatus";

import OrderCard from "../components/OrderCard";

function Orders() {
  const [orders, setOrders] = useState([]);

  const navigate = useNavigate();

  const fetchOrders = async () => {
    try {
      const res = await getMyOrders();

      setOrders(res.data.data || []);
    } catch (err) {
      console.log(err);

      if (err.response?.status === 401) {
        navigate("/login");
      }
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const cancelOrder = async (orderId) => {

    console.log("OrderId =", orderId);
    try {
      await cancelOrderService(orderId);

      alert("Order cancelled");
      fetchOrders();
    } catch (err) {
      console.log(err);
    }
  };

  const requestReturn = async (orderId) => {
    try {
      await requestReturnService(orderId);

      alert("Return requested");
      fetchOrders();
    } catch (err) {
      
          console.log(err);
          console.log(err.response);
          console.log(err.response?.data);

          alert(err.response?.data?.error || "Return failed");
      }
    }
  

  const downloadInvoice = async (orderId) => {
    try {
      const res = await downloadInvoiceService(orderId);

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", `invoice_${orderId}.pdf`);

      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
          console.log(err);
          console.log(err.response);
          console.log(err.response?.data);

          alert(err.response?.data?.error || "Download failed");
        }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>My Orders</h2>

      {Array.isArray(orders) &&
        orders.map((order) => (
          <OrderCard
            key={order.id}
            order={order}
            STATUS={STATUS}
            requestReturn={requestReturn}
            cancelOrder={cancelOrder}
            downloadInvoice={downloadInvoice}
          />
        ))}
    </div>
  );
}

export default Orders;