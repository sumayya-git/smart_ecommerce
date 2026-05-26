import { useEffect, useState } from "react";
import api from "./api";
import OrderProgress from ".../components/OrderProgress";

function MyOrders() {
 
  const [orders, setOrders] = useState([]);

  const handleCancel = async(orderId) => {
    try {
      
      await API.post(`order/cancel/${orderId}/`,{
        
        reason: "Customer cancelled from UI"
      });

    

    alert("Order Cancelled");
    window.location.reload();
      } catch(error){
        console.log(error);
      }
    };
  
    const handlePay =async (orderId) => {
      try {
       
        const res = await API.post(`order/pay/${orderId}/`);
          
        alert(res.data.message || res.data.error);

      window.location.reload();
    } catch(error) {
      console.log(error);
    }
  };

    

  useEffect(() => {
    api.get("my-orders/")
     .then((res) => {
        setOrders(res.data);
        console.log(res.data);
     })
     .catch((err) => {
        console.log(err);
        alert("Please login first");
     });
  },[]);

  
  return (
    <div>
        <h2>My Orders</h2>

        {Array.isArray(orders) && orders.length === 0 && ( <p>No orders found</p>)}

        {Array.isArray(orders) && orders.map((order) => {
          console.log("Order ID:", order.id, "Status:", order.status)

          return(

        
            <div key={order.id} style={{ border: "1px solid black",margin:"10px",padding:"10px"}}>
                <p><b>Order ID:</b> {order.id}</p>
                <p><b>Status:</b> {order.status}</p>

                <OrderProgress status={order.status} />

                {order.payment_status === "PAID" && (
                  <span style={{ color: "green", fontWeight:"bold"}}>
                    ✅Paid
                  </span>
                )}

                {order.status === "PLACED" && (
                  <button onClick={() => handlePay(order.id)}
                >
                  Pay Now
                </button>
                )}

                {["PLACED","PROCESSING"].includes((order.status|| "").trim().toUpperCase()) &&  (
                
                  <button onClick={() => handleCancel(order.id)}
                >
                  Cancel Order
                </button>
                )}

                <p><b>Total:</b> ${order.total_amount}</p>

                
                <h4>Items:</h4>
                {Array.isArray(order.items) && order.items.map((item) => (
                    <p key={item.id}>
                        {item.product_name} * {item.quantity}
                    </p>
                ))}
              </div>

        );
       })}
    </div>
  );
}

export default MyOrders;