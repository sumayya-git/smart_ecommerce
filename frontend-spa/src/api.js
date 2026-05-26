import axios from "axios";

const API=axios.create({
    baseURL:import.meta.env.VITE_API_BASE_URL,
    withCredentials: true,
   

   
    
});

function getCSRFToken(){
    const name = "csrftoken=";
    const cookies = document.cookie.split(";");


    for(let cookie of cookies){
        cookie = cookie.trim();
        if(cookie.startsWith(name)) {
            return cookie.substring(name.length);
        }
    }

    return null;
}

API.interceptors.request.use((config) => {
    const token = getCSRFToken();
     
     
     

    if (token) {
        config.headers["X-CSRFToken"] = token;

    }

   

    return config;
});


export default API;


    