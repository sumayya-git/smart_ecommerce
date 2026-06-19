import API from "../api"

export const loginUser = async(data) => {
    await API.get("/csrf/");

    const res = await API.post("/login/", data);

    console.log("LOGIN RESPONSE", res.data);

    const profile =  await API.get("/profile/");
    console.log("PROFILE AFTER LOGIN", profile.data);
    return res;
    // return API.post("/login/", data)
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

