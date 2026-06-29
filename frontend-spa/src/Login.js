import API from "../api";
import { useState } from "react";
// import { useNavigate } from "react-router-dom";

function Login() {
//  const[email, setEmail] = useState("");
 const[username, setUername] = useState("");
 const[password, setPassword] = useState("");

//  const navigate = useNavigate();

 const handleLogin = async () => {
   

   console.log("Login clicked");
   
  try {
     
    await API.post("/login/", {
     
        username:username,
        password:password,
      
      });
     

    

   
    

  
    
      await API.get("/csrf/");

      alert("Login successful✅");

      
      window.location.href = "/";

    

  } catch(err) {
    console.log(err);
    alert("Login failed ❌");
  }
};

return(
   <div>
    

   
        <h2>Login</h2>
         <input
          type="text"
          placeholder="Username"
          value = {username}
     
          onChange={(e) =>
            setUsername(e.target.value)}
          />
          <br /><br />

          <input
            type="password"
             placeholder="Password"
              value={password}
    
            onChange={(e) => 
              setPassword(e.target.value)}
             />
              <br/><br />

            <button onClick={handleLogin}>
              Login</button>
            
            </div>
 
     );
 } 

 

 export default Login;


