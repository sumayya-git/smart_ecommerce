function PaymentMethod({
  
    paymentMethod,setPaymentMethod}){


        return(
            <div style={{ marginBottom:"20px"}}>
            <h3> Select Payment Method</h3>

            <select value={paymentMethod} onChange={(e)=>setPaymentMethod(e.target.value)}>
                <option value="ONLINE">Online Payment</option>
                 <option value="COD">Cash on Delivery</option>
            </select>

            </div>
        )}



export default PaymentMethod


