import {useState} from "react";

import { useNavigate } from "react-router-dom";

import { registerUser } from "../services/authService";

import { toast } from "react-toastify";

function Register() {

    const [username,setUsername] = useState("");
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleRegister = async () => {

        setLoading(true);

        try {
            await registerUser(
            {
                username,
                email,
                password
            }
        );
            console.log("REGISTER SUCCESS");


            toast.success("User created");

            console.log("TOAST SUCCESS");
            navigate("/login");

            console.log("NAVIGATE SUCCESS")

    }catch (err){
        console.log(err);

        toast.error(err.response?.data?.message || "Something went wrong");

    } finally {
        setLoading(false);

    }
    };
    return(
        <div style={{padding:"40px"}}>
            <h2>Register</h2>

            <input placeholder="Username" onChange={(e)=>setUsername(e.target.value)} /><br/><br/>
            <input placeholder="Email" onChange={(e)=>setEmail(e.target.value)}/><br/><br/>
            <input type="password" placeholder="Password" onChange={(e)=>setPassword(e.target.value)}/><br/><br/>

            <button onClick={handleRegister} disabled={loading}>{loading ? "Registering...":"Register"}</button>

        </div>
    );
}

export default Register;
