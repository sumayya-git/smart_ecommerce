
import axios from "axios";

const API = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL,

    withCredentials: true,

    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
});

API.interceptors.request.use(
    (config) => {

        const token = document.cookie
            .match(/csrftoken=([^;]+)/)?.[1];

        if (token) {
            config.headers["X-CSRFToken"] = token;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

export default API;















