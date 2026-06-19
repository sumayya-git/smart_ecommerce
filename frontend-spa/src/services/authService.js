import API from "../api"

export const loginUser = async(data) => {
    await API.get("/csrf/");
    return API.post("/login/", data)
}


export const registerUser = (data) => {
    return API.post("/register/", data)
}


export const getProfile = async () => {
    return await API.get("/profile/")
}


export const logoutUser = async () => {

    await fetch("https://smart-ecommerce-gwjd.onrender.com/api/csrf/",
        {
            credentials: "include"
        }
    );
    return await API.post("/logout/");
}

