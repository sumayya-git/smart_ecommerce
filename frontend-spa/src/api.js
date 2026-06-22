import axios from "axios";

console.log(process.env.REACT_APP_API_BASE_URL);

const API=axios.create({
    baseURL:process.env.REACT_APP_API_BASE_URL,
    withCredentials: true,

    xsrfCookieName: "csrftoken",
    xsrfHeeaderName: "X-CSRFToken",
   

   
    
});

API.interceptors.request.use((config) => {

    const csrftoken = document.cookie 
        .split(";")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];

    console.log("COOKIE =", document.cookie);
    console.log("CSRF TOKEN =", token);
    if (csrftoken) {
        config.headers["X-CSRFToken"] = csrftoken;

    }

     return config;
});

export default API;











































// function getCSRFToken(){
//     const name = "csrftoken=";
//     const decodedCookie = decodeURIComponent(document.cookie);
//     const cookies = decodedCookie.split(";");


//     for(let cookie of cookies){
//         cookie = cookie.trim();
//         if(cookie.startsWith(name)) {
//             return cookie.substring(name.length);
//         }
//     }

//     return null;
// }
// console.log("COOKIE =", document.cookie);
// API.interceptors.request.use((config) => {

//     const token = document.cookie 
//         .split(";")
//         .find(row => row.startsWith("csrftoken="))
//         ?.split("=")[1];

//     console.log("COOKIE =", document.cookie);
//     console.log("CSRF TOKEN =", token);
//     if (token) {
//         config.headers["X-CSRFToken"] = token;

//     }

//      return config;
// });
    
    // console.log(document.cookie)
    // console.log(getCSRFToken())

    // const token = getCSRFToken();

    // console.log("CSRF TOKEN =", token)
     
     
     

    // if (token) {
    //     config.headers["X-CSRFToken"] = token;

    // }

   

    





    