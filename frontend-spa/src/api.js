import axios from "axios";

console.log(process.env.REACT_APP_API_BASE_URL);

const API=axios.create({
    baseURL:process.env.REACT_APP_API_BASE_URL,
    withCredentials: true,
   

   
    
});

function getCSRFToken(){
    const name = "csrftoken=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookies = decodedCookie.split(";");


    for(let cookie of cookies){
        cookie = cookie.trim();
        if(cookie.startsWith(name)) {
            return cookie.substring(name.length);
        }
    }

    return null;
}

API.interceptors.request.use((config) => {

    const token = document.cookie 
        .split(";")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
    if (token) {
        config.headers["X-CSRFToken"] = token;

    }

     return config;
});
    
    // console.log(document.cookie)
    // console.log(getCSRFToken())

    // const token = getCSRFToken();

    // console.log("CSRF TOKEN =", token)
     
     
     

    // if (token) {
    //     config.headers["X-CSRFToken"] = token;

    // }

   

    


export default API;


    