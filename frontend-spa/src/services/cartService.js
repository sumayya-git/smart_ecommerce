import API from "../api"

export const fetchCart = () => {
    return API.get("/cart/")
}


export const addToCart = (productId) => {
    return API.post(`/cart/add/${productId}/`)
}

export const removeCartItem = (itemId) => {
    return API.post(`/cart/remove/${itemId}/`)
}

export const decreaseCartItem = (productId) => {
    return API.post(`/cart/decrease/${productId}/`)
}


