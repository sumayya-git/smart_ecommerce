import React from "react";
import { useState, useEffect }  from "react";
// import "./App.css";
import {BrowserRouter as Router,Routes,Route} from "react-router-dom";
import Navbar from "./components/Navbar";
import CategoryHome from "./pages/CategoryHome";
// import Products from "./pages/Products";
import Cart from "./pages/Cart";
import Orders from "./pages/Orders";
import Login from "./pages/Login";
import AdminDashboard from "./AdminDashboard";
import AdminRoute from "./components/AdminRoute";

import PrivateRoute from "./components/PrivateRoute";

import ProductDetails from "./pages/ProductDetails";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import  EditProfile  from "./pages/EditProfile";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Checkout from "./pages/Checkout";
import CategoryProducts  from "./pages/CategoryProducts";
import API from "./api";

function App() {

  console.log(Register);
  console.log(Login);
  console.log(AdminDashboard);
  console.log(ToastContainer);
  console.log(Navbar);
  console.log(AdminRoute);
  console.log(PrivateRoute);
  console.log(EditProfile);
  console.log(Checkout);
  console.log(CategoryProducts);
  console.log(ProductDetails);



  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    API.get("/csrf/");

  },[]);

  
  const fetchCartCount = async () => {
    try{
      const res = await API.get("/cart/",{
      withCredentials: true,
    });

      const totalQty = res.data.data.items.reduce( (sum, item) => sum + item.quantity, 0);
    
    
      setCartCount(totalQty);
    

  } catch (err){
    console.log("Cart fetch skipped (not logged in)");
  }
};

useEffect(() => {
  const isLoggedIn = document.cookie.includes("sessionid");

  if(isLoggedIn) {

  
  fetchCartCount();
  }
},[]);

useEffect(() => {
    const handleCartUpdate = () => {
      fetchCartCount();
    };

    window.addEventListener("cartUpdated", handleCartUpdate);
    return () => {
    window.removeEventListener("cartUpdated", handleCartUpdate);
    };
  }, []);



 
    
  return (
    
    
    <Router>
      <Navbar cartCount={cartCount} refreshCart={fetchCartCount}/>
      <Routes>
        <Route path="/" element={<CategoryHome />} />
       
       
        <Route path="/cart" element={<PrivateRoute><Cart /></PrivateRoute>} />
        <Route path="/orders" element={<PrivateRoute><Orders /></PrivateRoute>} />
        <Route path="/login" element={<Login />} />
        <Route path="/product/:id" element={<ProductDetails refreshCart={fetchCartCount} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
        <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />

        <Route path="/edit-profile" element={<EditProfile />} />
        <Route path="/checkout" element={<PrivateRoute><Checkout /></PrivateRoute>} />
        <Route path="/category/:category" element={<CategoryProducts />} />
      </Routes>
         <ToastContainer position="top-right" autoClose={3000} />

    </Router>
    );
}
   
export default App;

