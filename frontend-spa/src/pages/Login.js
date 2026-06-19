import React,{ useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

// import { toast } from "react-toastify";


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

        console.log("COOKIE BEFORE LOGIN =", document.cookie);
        const res = await loginUser({
        
           username,
           password,
        });


        console.log("LOGIN RESPONSE =",res)

        console.log("COOKIE AFTER LOGIN =", document.cookie);
        

       
      
       

        window.dispatchEvent(new CustomEvent("userChanged",{
          detail:{
            username:username
          }
        }));
          
               

        

            // toast.success("Login success✅");

            // return;

            
            navigate("/")
           

            

            
  
      }catch(err){
        console.log(err)

        
            
        // toast.error(err.response?.data?.message);
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

        <button type="submit" disabled={loading}>{loading ? "Logging on...": "Login"}</button>


       </form>
    
);
}

export default Login;
        