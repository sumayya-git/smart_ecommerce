import React, {useState, useEffect} from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import API from "../api";

function EditProfile(){
    const [phone,setPhone] = useState("");
    const [address,setAddress] = useState("");
     const [city,setCity] = useState("");
      const [state,setState] = useState("");
       const [pincode,setPincode] = useState("");

       const navigate = useNavigate();

       useEffect(() => {
       
        API.get("/profile/")
           

            .then(res=>{
                setPhone(res.data.phone || "")
                setAddress(res.data.address || "")
                setCity(res.data.city || "")
                setState(res.data.state || "")
                    setPincode(res.data.pincode || "")
            })
            .catch(err=>{
                console.log(err);

             if(err.response?.status === 401) {
                alert("Please login first");
                navigate("/login");
             }

       });

    },[]);

        const handleSave = async () => {
        try {
                                  
        

            await API.post("/update-profile/",
                {
                    phone,
                    address,
                    city,
                    state,
                    pincode
                });
                
            
            toast.success("Profile Updated Successfully",{autoClose:1200});
            

             setTimeout(()=>{
                navigate("/profile");
             },1200);
            
            
             
        } catch(err){
            console.log(err);
            toast.error("Update failed");

             if(err.response?.status === 401) {
                navigate("/login");

        }
        }
    };

        return(
            <div style={{padding:"20px"}}>
                <h2>Edit Profile</h2>

                <input placeholder="Phone" value={phone} onChange={(e)=>setPhone(e.target.value)}/>
                <br/><br/>

                <input placeholder="Address" value={address} onChange={(e)=>setAddress(e.target.value)}/>
                <br/><br/>
                <input placeholder="City" value={city} onChange={(e)=>setCity(e.target.value)}/>
                <br/><br/>
                <input placeholder="State" value={state} onChange={(e)=>setState(e.target.value)}/>
                <br/><br/>
                <input placeholder="Pincode" value={pincode} onChange={(e)=>setPincode(e.target.value)}/>
                <br/><br/>

                <button onClick={handleSave}>
                    Save Profile
                </button>
            </div>
        );
}
export default EditProfile;