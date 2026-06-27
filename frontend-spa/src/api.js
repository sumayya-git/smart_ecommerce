import axios from "axios";

const API=axios.create({
    baseURL:process.env.REACT_APP_API_BASE_URL,
    withCredentials: true,

    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
   

   
    
});

console.log("BASE URL =", process.env.REACT_APP_API_BASE_URL);

console.log("API.JS LOADED");
console.log(API.defaults);

API.interceptors.request.use((config) => {
     
      console.log("INTERCEPTOR RUNNING");

      const match = document.cookie.match(/csrftoken=([^;]+)/);
      const csrftoken = match ? match[1] : null;

      console.log("CSRF TOKEN =", csrftoken);
        if (csrftoken) {
            config.headers["X-CSRFToken"] = csrftoken;

        }
      console.log("FINAL HEADERS =", config.headers.toJSON());
      return config;
 });

export default API;



































// API.interceptors.request.use((config) => {
//     console.log("INTERCEPTOR RUNNING");

//     console.log("ALL COOKIES =", document.cookie);

//     const match = document.cookie.match(/csrftoken=([^;]+)/);

//     const csrftoken = match ? match[1] : null;

//     // const csrftoken = document.cookie 
//     //     .split(";")
//     //     .find(row => row.startsWith("csrftoken="))
//     //     ?.split("=")[1];

    
//     console.log("CSRF TOKEN =", csrftoken);
//     if (csrftoken) {
//         config.headers["X-CSRFToken"] = csrftoken;

//     }

//      return config;
// });













































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

   

    





    