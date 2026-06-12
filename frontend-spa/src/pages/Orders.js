// import React,{ useEffect, useState } from "react";
// // import OrderProgress from  "../components/OrderProgress";

// import { useNavigate } from "react-router-dom";

// import { getMyOrders, cancelOrderService, requestReturnService, downloadInvoiceService } from "../services/orderService"

// import STATUS from "../constants/orderStatus"

// import OrderCard from "../components/OrderCard"


//  console.log(OrderCard);
// //  console.log(OrderProgress);
//  console.log("STATUS =", STATUS);
//  console.log(useNavigate)




import React  from "react"
function Orders() {
  return (
    <div>HELLO ORDERS</div>
  );
}
  

//     const [orders, setOrders] = useState([]);

//      console.log("orders =", orders);
//      console.log("OrderCard =", OrderCard);


//     const navigate = useNavigate();

   
   

//     const fetchOrders = async () => {
//      try{
      
    
        
    
           
//            const res = await getMyOrders()
          
           
      
    
       
            
//             setOrders(res.data.data || [])
            

            
         
//      }catch(err){
//       console.log(err);

//       if(err.response?.status === 401){
//          navigate("/login");
//      }
            
//     }
//     }
  

//      useEffect(() => {
//        fetchOrders();
//      }, []);
    
//      const cancelOrder = async (orderId) => {
//       try{
       

//        await cancelOrderService(orderId)
  
//         alert("Order cancelled");
//         fetchOrders();
        
//     }catch(err){
//       console.log(err);
//     }
       
   
        
// };

// const requestReturn = async (orderId) => {
//   try{
//     await requestReturnService(orderId)
      

//     alert("Return requested");
//    fetchOrders();
//   } catch (err) {
//     alert("Return failed");
//   }
  
// }

//   const downloadInvoice = async (orderId) => {
    
//     try{
    

//       const res = await downloadInvoiceService(orderId)
//       const url = window.URL.createObjectURL(new Blob([res.data]));
//       const link = document.createElement("a");
//       link.href = url
//       link.setAttribute("download", `invoice_${orderId}.pdf`);
//       document.body.appendChild(link);
//       link.click();
//       link.remove();

//     } catch(err) {
     
//       alert(" Download failed");
//     }
//   }
    
    
// return(

  
//     <div style={{ padding: "20px" }}>
//        <h2>My Orders</h2>
       
    
//         {Array.isArray(orders) && orders.map((order) => (
          
//           <div key={order.id}>
//              Order ID: {order.id}
//              </div>
    
        
//           // <OrderCard key={order.id}
//           //   order={order}
//           //   STATUS={STATUS}
//           //   requestReturn={requestReturn}
//           //   cancelOrder={cancelOrder}
//           //   downloadInvoice={downloadInvoice} />

//         ))}

//       </div>
//       )
//     }
          
          
                 
                                               
                               
    
  export default Orders
    
        



