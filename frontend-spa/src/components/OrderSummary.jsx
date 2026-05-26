function OrderSummary({
  
    totalAmount,placeOrder}){


        return(
            <div style={{ marginTop:"20px"}}>
            <h3> Total: ${totalAmount}</h3>

            <button onClick={placeOrder}
              style={{
                background:"orange",
                color:"white",
                padding:"10px 20px",
                border:"none",
                cursor:"pointer"
                }}>
            
                Place Order
            </button>
        </div>
        )}



export default OrderSummary


