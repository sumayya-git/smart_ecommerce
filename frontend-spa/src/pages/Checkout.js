import { useState, useEffect } from "react";

import { useNavigate } from "react-router-dom";
import { fetchCart } from "../services/cartService"

import { createOrder } from "../services/orderService"

import PaymentMethod from "../components/PaymentMethod";

import OrderSummary from "../components/OrderSummary";

import AddressForm from "../components/AddressForm";

import { toast } from "react-toastify";


function Checkout(){
  
    const [paymentMethod,setPaymentMethod] = useState("COD");

    const [address, setAddress] = useState("")
    const navigate = useNavigate();

    const [cart,setCart] = useState([])


    useEffect(() => {


        const loadCart = async () => {
         try{
            

            const cartRes = await fetchCart()


            const cartItems = cartRes.data.data.items || []

            console.log("CHECKOUT CART:", cartItems)


            setCart(cartItems)

        }catch(err){
            console.log(err)
        }
    }

               
               

            loadCart()
            
            
            
            
        },[])



    const totalAmount = cart.reduce((total, item) =>  
                total + ((item.product?.price || item.product_price || 0) * item.quantity),0)

   


     
    const placeOrder = async () => {

          
        
        try{
           
            
      

            

         

            if(cart.length === 0){
                toast.info("Cart is empty");

                return;
            }


           
        
       
              
                    
                    if (paymentMethod === "COD"){
                        
                

                                 
                        const finalItems = cart.map(item => ({
                                product_id:item.product?.id || item.product_id || item.id,
                                quantity: item.quantity,
                            }));

                         
                         const res = await createOrder({
                                
                            items: finalItems,
                            address: address,
                            payment_method: "COD",
                            amount: totalAmount,
                            });

                            console.log(res);

                            

                            
                            

                
               
                   
            
                                toast.success("Order placed successfully");

                                window.dispatchEvent(new Event("cartUpdated"));

                                setTimeout(() => {

                                

                                  navigate("/orders");

                                }, 500);

                           
                              

                                
               
                

               
}
            

            }catch(err){
                console.log("ERROR:",err.response?.data || err);
                if (err.response?.status === 401 || err.response?.status === 403) {
                    toast.warning("Please login first ❌");
                    navigate("/login");
            }
                toast.error(err.response?.data?.error || "Something went wrong")
        }
        };
        
    

    return(
        <div style={{padding:"20px"}}>
            

           <PaymentMethod paymentMethod={paymentMethod}
                        setPaymentMethod={setPaymentMethod}
                        />

            <AddressForm address={address}
                    setAddress={setAddress}/>


            <OrderSummary totalAmount={totalAmount}
                placeOrder={placeOrder}/>



            
        </div>

    );
}

export default Checkout;