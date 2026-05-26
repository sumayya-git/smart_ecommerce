import React, {useEffect, useState} from "react";
import API  from "../api";
// import { useNavigate } from "react-router-dom";

function Profile(){
    const [profile, setProfile] = useState(null);
    

    useEffect(()=>{
        const fethProfile = async () => {
            try {
                
                const response = await  API.get("/profile/");

                 
                setProfile(response.data)
                console.log("PROFILE DATA:", response.data);
            } catch  (error) {
                console.error("Error Fetching profile:", error);
            }
        };

          fethProfile();
    }, []);

    if(!profile) return <h2>Loading...</h2>;

    return(
        <div>
            <h1>My Profile</h1>

            

            <p>Username:{profile.username}</p>
            <p>Email: {profile.email}</p>
            <p>Phone:         
                 {profile.phone}</p>
                  <p>Address:           
                 {profile.address}</p>
                 <p>City:          
                 {profile.city}</p>
                 <p>State:           
                 {profile.state}</p>

                 <p>Pincode:          
                 {profile.pincode}</p>


                    

              
        </div>
    );
}

export default Profile;