import { useParams }  from "react-router-dom";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

import { fetchProductDetails } from "../services/productService"; 

import  { addToCart } from "../services/cartService"; 

// import { toast } from "react-toastify";


function ProductDetails({refreshCart}){
    
    const {id} = useParams();
    const navigate = useNavigate();

    const [product, setProduct] = useState(null);

    const [loading, setLoading] =useState(true);

    const [cartLoading, setCartLoading] = useState(false);

    useEffect(() => {
        fetchProductDetails(id)

            
            .then((res) => { 
                setProduct(res.data);
            })
            .catch((err) => {
                console.log(err);

            })
            .finally(() => {
                setLoading(false);
            });
        }, [id]);

    const handleAddToCart = async () => {

        if (!product) return;

        if (product.stock === 0) {
            // toast.warning("Out of stock ❌");
            return;
        }
        
        
        setCartLoading(true);
       
    
        try {
            
              await addToCart(product.id, 1)
                 
                   
                 
               
            

            refreshCart();

                 alert("added to cart");
            
            //    toast.success("Added to cart 🛒");

               window.dispatchEvent(new Event("cartUpdated"));
                
        } catch (err) {
            console.log(err);

            if (err.response?.status === 401) {
                // toast.warning("Please login first");
                navigate("/login");
            } else {
             
            // toast.error("Error ❌");
        }

    } finally {
        setCartLoading(false);
    }
    
        };
    

    //     const handleBuyNow = async () => {
    //         if(!product) return;
    //         if(product.stock === 0) {

    //             //  toast.warning(" out of stock ❌");
    //             return;
    //         }
            

    //          setCartLoading(true);
    //          try {

                
            
              
           
    //               await addToCart(product.id, 1)
                  

    //               window.dispatchEvent(new Event("cartUpdated"));

           
          
    //              navigate("/checkout");
    //         } catch (err) {
    //             console.log(err);
                
    //             if(err.response?.status === 401) {
    //                 // toast.warning("Login first");
    //                 navigate("/login");
    //             } else {
             
    //             //   toast.error("Error ❌");
    //             }

    //         } finally{
    //             setCartLoading(false);
    //       }
        
    //     };




    

    if(loading){
        return ( <h2 style={{padding:"20px"}}
        >Loading...</h2>);
    }

    console.log(product);


    const handleBuyNow = () => {

    if (!product) return;

    if (product.stock === 0) {
        return;
    }

    navigate("/checkout", {
        state: {
            buyNow: true,
            product: {
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image,
                stock: product.stock,
            },
            quantity: 1,
        },
    });

};

    return(
        <div style={{padding:"20px"}}>
            {product.image && (
              <img src={product.image}
                alt={product.name}
                style={{
                    width:"300px",
                    height:"300px",
                    objectFit:"contain",
                    border:"1px solid #ddd"
                }}
                
             />
            )}
            <h2>{product.name}</h2>
             <p>Price: ${product.price}</p>
            
             <p>{product.description}</p>

             

                  {product.stock === 0 ? (
                    <p style={{
                     
                      color:"red",
                      fontWeight: "bold",
                      fontSize: "16px",
                      marginTop:"10px"
                    }}>
                   
                     ❌ This item is Currently unavailable
                   </p>
                  ):(
                    <>
                                                                <p
                            style={{
                                color: product.stock <= 5 ? "#ff8c00" : "green",
                                fontWeight: "700",
                                fontSize: "16px",
                                marginTop: "8px",
                                marginBottom: "12px"
                            }}
                        >
                            {product.stock <= 5
                                ? `Only ${product.stock} left in stock ⚠️`
                                : "In Stock✅"}
                        </p>
                     <button 
                       
                        onClick={handleAddToCart} disabled={cartLoading}
                            


               
                        style={{
                            
                        
                        
                            background:"#007bff",
                            color:"white",
                            padding:"8px 16px",
                            border:"none",
                            borderRadius:"4px",
                            marginRight:"10px",
                            cursor:"pointer"
                        }}

                     >
                        {cartLoading ? "Adding...": "Add to Cart"}
                            
                        </button>



                        <button onClick={handleBuyNow} disabled={cartLoading}
                           
                            style={{
                                background: product.stock === 0 ? "#ccc": "#ffa41c",
                                cursor: product.stock === 0 ? "not-allowed": "pointer",
                            
                            
                                background:"#ffa41c",
                                color:"white",
                                padding:"8px 15px",
                                border:"none",
                                marginLeft:"10px",
                                cursor:"pointer"
                            }}
                            >
                                {cartLoading ? "Processing...": "Buy Now"}
                                
                            </button>
                            </>
                            )}
                   
        </div>
    );

}
export default ProductDetails;