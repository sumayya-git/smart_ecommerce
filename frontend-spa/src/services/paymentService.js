import API from "../api"



export const verifyPayment = (data) => {
    return API.post("/verify-payment/", data)
}


