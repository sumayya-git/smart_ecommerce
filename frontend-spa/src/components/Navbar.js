import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom"


import { FaChevronDown } from "react-icons/fa";
import { FaBars } from "react-icons/fa";

import { getProfile, logoutUser } from "../services/authService";

import { fetchCart } from "../services/cartService";



function Navbar({ cartCount, refreshCart }) {

  const navigate = useNavigate();

  useEffect(() => {
   

  }, []);

  const [showDropdown, setShowDropdown] = useState(false);
  const [search, setSearch] = useState("");
  
  const [showMenu, setShowMenu] = useState(false);

  

  const [username,setUsername] = useState(null);


  useEffect(() => {
    getProfile()
    .then((res) => {
      setUsername(res.data.username);

    })
    .catch(() => {
      setUsername(null);
    });
  }, []);

  useEffect(() => {
    loadCart();
  }, []);

 

  useEffect(() => {
    const handleUserChange = (e) => {
      console.log("EVENT RECEIVED:", e.detail);
      if(e.detail)  { 

      
        setUsername(e.detail.username);
      }
    };

    
    window.addEventListener("userChanged", handleUserChange);
    
    return () => {
      window.removeEventListener("userChanged",handleUserChange);
    };
  },[]);


  useEffect(() => {
    const handleCartUpdate = () => {
      loadCart();
    };

    window.addEventListener("cartUpdated", handleCartUpdate);
    return () => {
    window.removeEventListener("cartUpdated", handleCartUpdate);
    };
  }, []);

  

    const loadCart =  async () => {
      try{
        const res = await fetchCart()
         
        

        console.log("CART DATA:", res.data);

        if(refreshCart) {
          refreshCart(res.data.data.items.length || 0);
        }
      } catch(err){
        console.log("Cart error", err);
      }
    };

   

   
  
  
    
    
  const logout = async () => {
    
    try {
     
      await getProfile()
      
      await logoutUser()
       
        
        
        
    
   
   

   

    
   
    window.location.href="/login";
    } catch (err) {
      console.log("Logout error:",err);
    }
  };

 

    
  return (
    <>
    
      
        <div style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            backgroundColor: "#131921",
            padding: "10px 20px",
            color: "white",
            
        }}>

            {/*Logo*/}
            <div>
            <h2 style={{ color:"#febd69", margin: 0 }}>SmartShop</h2>
            <div style={{
              height:"4px",
              width:"80px",
              backgroundColor:"#febd69",
              borderRadius:"50%",
              marginTop:"2px"
            }}></div>
            </div>

            {/*Search */}
             <div style={{ display: "flex", width:"50%"}}>

                <input type="text"
                  placeholder="Search products..." 
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  style={{
                    width:"100%",
                    padding:"10px",
                    border:"none",
                    outline:"none"
                   }}
                  />
                  </div>
                  
              

               <div style={{ display: "flex", gap:"20px", alignItems:"center" }}>
                  <div 
                      style={{ position: "relative",
                          cursor:"pointer"}}
                       onMouseEnter={() =>
                       setShowDropdown(true)}
                       onMouseLeave={() =>
                         setShowDropdown(false)}>
                        
            
                      <div style={{ fontSize: "12px" }}>Hello,{username ? username : "Guest"}</div>

                      <div style={{ fontWeight: "bold" }}>
                         Account & Lists
                         </div>
                         
                        {showDropdown && (
                          <div
                             
                            style={{
                            position:"absolute",
                            top:"100%",
                            right:"0",
                            
                            width:"250px",
                            background: "white",
                            color:"black",
                            padding:"15px",
                            boxShadow:"0px 4px 15px rgba(0,0,0,0.1)",
                            
                            borderRadius: "6px",
                            zIndex: 1000,
                          }}
                        >
                          {!username ? (
                            <>
                            <button style={{
                                width: "100%",
                                padding:"10px",
                                backgroundColor:"#febd69",
                                border:"none",
                                
                                
                                cursor:"pointer",
                                
                               
                                
                            }}

                             onClick={() => navigate("/login")}
                              >
                                Sign in
                              </button>
                       
                        
                             

                              <p style={{ marginTop:"10px"}}>
                                New customer?{" "}
                                <span style={{ color: "#007185", cursor:"pointer" }}
                                  onClick={() => navigate("/register")}
                                  >
                                  Start here</span>
                              </p>
                            
                            </>
                          ):(
                          <p style={{
                              marginTop:"10px",
                              cursor:"pointer",
                              color:"red",
                            }}
                            onClick={logout}
                            >
                              Logout
                            </p>
                          )}
                          <hr />
                          <div style={{ display:"flex", gap:"20px"}}>
                          <div>
                            <h4>Your Lists</h4>
                            <p>Wish List</p>
                            <p>Baby Wishlist</p>
                           
                          </div>
                          <div>
                            <h4>Your Account</h4>
                            <p onClick={() => navigate("/profile")}>My Profile</p>

                            <p>Your Orders</p>
                            <p>Your Wishlist</p>
                            
                          </div>
                          </div>
                          
                            
                          </div>
                        )}
                        </div>

                        <div style={{ cursor:"pointer" }} onClick={() => 
                           navigate("/orders")}>
                          Orders
                        </div>

                        <div style={{ cursor:"pointer" }} onClick={() => 
                            navigate("/cart")}>
                          Cart({cartCount})
                        </div>

                                           
                        </div>
                        </div>
                                    
                                                                   
                         
                                
                              
                 <div style={{ 
                    display: "flex",
                      gap:"20px" ,
                       backgroundColor:"#232f3e",
                        color: "white",
                         padding: "10px 20px",
                         
                 }}>
                  <p style={{ cursor:"pointer"}}>
                    <FaBars /> All
                  </p>
                  <p>Today's Deals</p>
                  <p>Mobiles</p>
                  <p>Laptops</p>
                  <p>Accessories</p>
                  </div>
                  
                  </>
                  
                  
                  
    );
  }

export default Navbar;