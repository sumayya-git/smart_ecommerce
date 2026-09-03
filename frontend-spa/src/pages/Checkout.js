import { useState, useEffect } from "react";

import { useNavigate, useLocation } from "react-router-dom";
import { fetchCart } from "../services/cartService"

import { createOrder } from "../services/orderService"

import PaymentMethod from "../components/PaymentMethod";

import OrderSummary from "../components/OrderSummary";

import AddressForm from "../components/AddressForm";

import API from "../api";

// import { toast } from "react-toastify";


function Checkout(){
  
    const [paymentMethod,setPaymentMethod] = useState("COD");

    const [address, setAddress] = useState("")
    const navigate = useNavigate();
    const location = useLocation();

    const [cart,setCart] = useState([])

    const buyNowData = location.state;


    // useEffect(() => {


    //     const loadCart = async () => {
    //      try{
            

    //         const cartRes = await fetchCart()


    //         const cartItems = cartRes.data.data.items || []

    //         console.log("CHECKOUT CART:", cartItems)


    //         setCart(cartItems)

    //     }catch(err){
    //         console.log(err)
    //     }
    // }

               
               

    //         loadCart()
            
            
            
            
    //     },[])

    useEffect(() => {

    if (buyNowData?.buyNow) {

        setCart([
            {
                product: buyNowData.product,
                quantity: buyNowData.quantity
            }
        ]);

        return;
    }

    const loadCart = async () => {

        try {

            const cartRes = await fetchCart();

            const cartItems = cartRes.data.data.items || [];

            console.log("CHECKOUT CART:", cartItems);

            setCart(cartItems);

        } catch (err) {

            console.log(err);

        }

    };

    loadCart();

}, [buyNowData]);


    const totalAmount = cart.reduce((total, item) =>  
                total + ((item.product?.price || item.product_price || 0) * item.quantity),0);


    const isBuyNow = buyNowData?.buyNow === true;
   


     
    const placeOrder = async () => {

          
        
        try{
           
            
      

            

         

            if(cart.length === 0){
                // toast.info("Cart is empty");

                return;
            }

            if (paymentMethod === "ONLINE") {

                                // Create Razorpay Order
                                const paymentRes = await API.post(
                                    "/payment/create-order/",
                                    {
                                        amount: totalAmount
                                    }
                                );

                                const orderData = paymentRes.data.data;

                                

                                console.log("KEY =", process.env.REACT_APP_RAZORPAY_KEY_ID);


                                const options = {
                                    key: process.env.REACT_APP_RAZORPAY_KEY_ID,

                                    amount: orderData.amount,

                                    currency: "INR",

                                    name: "Smart Commerce",

                                    description: "Order Payment",

                                    order_id: orderData.razorpay_order_id,

                                    handler: async function (response) {

                                        await API.post("/verify-payment/", {

                                                order_id: orderData.razorpay_order_id,

                                                razorpay_order_id: response.razorpay_order_id,

                                                razorpay_payment_id: response.razorpay_payment_id,

                                                razorpay_signature: response.razorpay_signature,

                                                address: address,

                                                buy_now: isBuyNow,

                                                product_id: isBuyNow ? buyNowData.product.id : null,

                                                quantity: isBuyNow ? buyNowData.quantity : null

                                            });
                                        window.dispatchEvent(new Event("cartUpdated"));

                                        navigate("/orders");
                                    },

                                    theme: {
                                        color: "#3399cc"
                                    }
                                };

                                const rzp = new window.Razorpay(options);

                                rzp.open();
                            }


           
        
       
              
                    
                    if (paymentMethod === "COD"){
                        
                

                                 
                        // const finalItems = cart.map(item => ({
                        //         product_id:item.product?.id || item.product_id || item.id,
                        //         quantity: item.quantity,
                        //     }));


                                                let finalItems;

                        if (isBuyNow) {

                            finalItems = [
                                {
                                    product_id: buyNowData.product.id,
                                    quantity: buyNowData.quantity,
                                }
                            ];

                        } else {

                            finalItems = cart.map(item => ({
                                product_id: item.product?.id || item.product_id || item.id,
                                quantity: item.quantity,
                            }));

                        }


                    

                         
                         const res = await createOrder({
                                
                            items: finalItems,
                            address: address,
                            payment_method: "COD",
                            amount: totalAmount,
                            });

                            console.log(res);

                            console.log("Order Response:", res.data);

                            const cartRes = await fetchCart();
                            console.log("Cart After Order:", cartRes.data);

                            console.log("BEFORE EVENT");

                            
                            

                            

                           
                                                        

                            
                            

                
               
                   
            
                                // toast.success("Order placed successfully");

                                window.dispatchEvent(new Event("cartUpdated"));

                                console.log("BEFORE NAVIGATE");

                                setTimeout(() => {

                                

                                  navigate("/orders");

                                   console.log("AFTER NAVIGATE");


                                }, 500);

                           
                              

                                
               
                

               
}
            

            }catch(err){
                console.log("ERROR:",err.response?.data || err);
                if (err.response?.status === 401 || err.response?.status === 403) {
                    // toast.warning("Please login first ❌");
                    navigate("/login");
            }
                // toast.error(err.response?.data?.error || "Something went wrong")
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