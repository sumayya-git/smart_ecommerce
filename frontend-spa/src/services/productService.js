import API from "../api"



export const fetchProducts = () => {
    return API.get("/products/")
}

export const fetchProductDetails = async(id) => {
    return await API.get(`/products/${id}/`)
}

