import API from "../api"



export const createOrder = async (data) => {
    return await API.post("/order/create/", data)
}

export const fetchOrders = async () => {
    return await API.get("/orders/")
}

export const getMyOrders = async () => {
    return await API.get("/my-orders/")
}

export const cancelOrderService = async (orderId) => {
    return await API.post(`/order/cancel/${orderId}/`);
}


export const requestReturnService = async (orderId) => {
    console.log("SERVICE orderId =", orderId);
    return await API.post(`/order/${orderId}/return/`)
}

export const downloadInvoiceService = async (orderId) => {
    return await API.get(`/order/${orderId}/invoice/`,{
        responseType:"blob"
    })
}





