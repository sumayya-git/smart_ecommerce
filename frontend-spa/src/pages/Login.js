import React,{ useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

import { toast } from "react-toastify";


const getCookie = (name) => {
  let value = null;
  if(document.cookie) {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if(cookie.startsWith(name + "=")) {
        value = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return value;
};

function Login() {

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate();

    const getCSRFToken = () => {
      return document.cookie .split(";") .find((row) => row.startsWith("csrftoken=")) ?.split("=")[1];
    }

    const handleLogin = async (e)=> { 
      e.preventDefault();
      console.log("Login clicked");
      
      try{
        setLoading(true)
        await loginUser({
        
           username,
           password,
        })

       
      
       

        window.dispatchEvent(new Event("userChanged"));
          
               

        

            toast.success("Login success✅");

            
            navigate("/")
           

            

            
  
      }catch(err){
        console.log(err)

        
            
        toast.error(err.response?.data?.message);
        }

        finally{
          setLoading(false)
        }
};
        
return(
  <form onSubmit={handleLogin}>
    
       <h2>Login</h2>

      
        
            <input type="text" placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
               required
              />

        
        <br /><br />

        
            <input type="password" placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
               required
              />

        
        <br /><br />

        <button type="submit" disabled={loading}>{loading ? "Loggingvon...": "Login"}</button>


       </form>
    
);
}

export default Login;
        