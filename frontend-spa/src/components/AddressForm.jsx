function AddressForm({
  
   address,setAddress}){


        return(
            <div style={{ marginBottom:"20px"}}>
             <h3> Delivery Address</h3>

             <textarea value={address}
                 onChange={(e) => setAddress(e.target.value)}

                 rows="4"
                 cols="40"
                 placeholder="Enter address"
                 />

            </div>
        )
   }

            



export default AddressForm


