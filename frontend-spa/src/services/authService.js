import API from "../api"

export const loginUser = async(data) => {
    await API.get("/csrf/");

    const res = await API.post("/login/", data);

   

    

   
};


export const registerUser = (data) => {
    return API.post("/register/", data)
};


export const getProfile = async () => {
    return await API.get("/profile/");
};


export const logoutUser = async () => {

   return await API.post("/logout/");
    


};

