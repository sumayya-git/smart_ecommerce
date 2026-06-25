import API from "../api"

function getCSRFToken() {

    console.log("ALL COOKIES =", document.cookie);

    const match = document.cookie.match(/csrftoken=([^;]+)/);

    return match ? match[1]:"";
}
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; csrftoken=`);
//     if (parts.length === 2) {
//         return parts.pop().split(";").shift();

//     }
//     return "";
// }

console.log(API.defaults.xsrfCookieName);
console.log(API.defaults.xsrfHeaderName);

export const fetchCart = () => {
    return API.get("/cart/")
}


export const addToCart = async (productId, quantity) => {

    console.log("ADD TO CART FUNCTION CALLED");

    const csrftoken = document.cookie
        .split(';')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    console.log("TOKEN =", csrftoken);

    

    // console.log("CSRFTOKEN =", csrftoken);

    console.log("ABOUT TO SEND REQUEST");

    return await API.post(`/cart/add/${productId}/`, { quantity },
        {
            headers: {
                "X-CSRFToken": csrftoken
            }
        }
       
    );
}

export const removeCartItem = (itemId) => {

    // const csrftoken = getCSRFToken();

    return API.post(`/cart/remove/${itemId}/`,
        {},
        // {
        //     headers: {
        //         "X-CSRFToken": csrftoken
        //     }
        // }
    );
}

export const decreaseCartItem = (productId) => {

    //  const csrftoken = getCSRFToken();
     
     
     return API.post(`/cart/decrease/${productId}/`,

        {},
        // {
        //     headers: {
        //         "X-CSRFToken": csrftoken
        //     }
        // }
    );

}


