// import OrderProgress from "./OrderProgress"
// import PaymentBadge from "./PaymentBadge"
// import OrderItem from "./OrderItem"


// console.log("OrderItem =", OrderItem);
// console.log("PaymentBadge =", PaymentBadge);
// console.log("OrderProgress =", OrderProgress);


function OrderCard({
    order,
    STATUS,
    requestReturn,
    cancelOrder,
    downloadInvoice
}) {
    const refundStatus =
      (order.refund_status || "").toLowerCase().trim()

    
    const returnStatus =
      (order.return_status || "").toLowerCase().trim()


    const orderStatus =
      (order.status || "").toLowerCase().trim()

      console.log("order =", order)




    return(
      <div>
        TEST
      </div>
        // <div style={{
        //     border: "1px solid #ccc",
        //     padding: "15px",
        //     marginBottom: "20px",
        //     borderRadius: "10px"
        // }}

        // >
        //     <h3>
        //         Order ID: {order.id}
        //     </h3>


        //     <div style={{ display: "flex", alignItems: "center", gap: "10px"}}>
        //        <p>Status: {order.status}</p>

        //        {/* <PaymentBadge order={order} /> */}
        // </div>

        // {/* <OrderProgress status={order.status} /> */}

        // {refundStatus === STATUS.INITIATED && (
        //           <p style={{color:"orange", fontWeight:"bold"}}>Refund Initiated 💰</p>)}

        //         {refundStatus === STATUS.COMPLETED && (
        //           <p style={{color:"green", fontWeight:"bold"}}>Refund Completed 💸</p>)}

        //         {returnStatus === STATUS.REQUESTED && (
        //           <p style={{color:"orange", fontWeight:"bold"}}>Return Requested ⌛</p>)}

        //         {returnStatus === STATUS.APPROVED && (
        //           <p style={{color:"green", fontWeight:"bold"}}>Return Approved ✅</p>)}

        //         {orderStatus === STATUS.DELIVERED && returnStatus === "none" && (
        //                 <button onClick={() => requestReturn(order.id)}>

                          
        //                        Return Order</button>)}


        //          {(order.payment_method.toUpperCase() === "ONLINE" ||  order.payment_method.toUpperCase() === "COD") && (

        //             <div style={{ marginTop: "10px" }}>
        //             <button onClick={() => 
                              
        //                downloadInvoice(order.id)}>
        //                 Download Invoice
        //            </button>
            
                                      
        //            </div>
                      
        // )}


        // <p><b>Method:</b>{""} {order.payment_method}</p>
        //           <p><b>Payment Status:</b>{""} {order.payment_status}</p>
                  
        //           <p><b>Total: </b>{""}${order.total}</p>

        //       <div style={{ marginTop: "10px"}}>
        //         <b>Timeline:</b>

        //       {order.placed_at && (<p>✅Placed:{""} {new Date(order.placed_at).toLocaleString()}</p>)}
        //       {order.packed_at && (<p>📦Packed: {""} {new Date(order.packed_at).toLocaleString()}</p>)}
        //       {order.shipped_at && (<p>🚚Shipped:{""} {new Date(order.shipped_at).toLocaleString()}</p>)}
        //       {order.delivered_at && (<p>💐Delivered: {""} {new Date(order.delivered_at).toLocaleString()}</p>)}
        //     </div>

            
        //       <div style={{ marginTop: "15px" }}>

        //          <h3>Items:</h3>

        //          {/* {Array.isArray(order.items) && order.items.map((item,index) => (

        //             <OrderItem key={index} item={item}/>
        //          ))} */}

        //          </div>
                    
                      

           

        //        {["PLACED","PROCESSING"].includes((order.status|| "").trim().toUpperCase()) &&  (
                
        //           <button onClick={() => cancelOrder(order.id)}
        //         >
        //           Cancel Order
        //         </button>
        //         )}
               

        //          </div>





        
               
    )
}

export default OrderCard