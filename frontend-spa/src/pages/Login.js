import React,{ useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";



function Login() {

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate();

   
    const handleLogin = async (e)=> { 
     
      e.preventDefault();
      console.log("Login clicked");
      
      try{
        setLoading(true)

       
        await loginUser({
        
           username,
           password,
        });

        
        

       
      
       

        window.dispatchEvent(new CustomEvent("userChanged",{
          detail:{
            username:username,
          },
        }));
          

        
        
              
               

        

            // toast.success("Login success✅");

            // return;

            
            navigate("/");
           

            

            
  
      }catch(err){
        console.log(err);

        
            
        // toast.error(err.response?.data?.message);
        }

        finally{
          setLoading(false);
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
        