import { useEffect, useState } from "react";
import { fetchCart, addToCart, removeCartItem, decreaseCartItem } from "../services/cartService";
import { useNavigate } from "react-router-dom";

import { toast } from "react-toastify";

function Cart() {

  const [cart, setCart] = useState({ items: [] });


  const [loading, setLoading] = useState(true);

  const [cartLoading, setCartLoading] = useState(false);

  const [removeLoading, setRemoveLoading] = useState(false);

  const navigate = useNavigate();



  const loadCart = async () => {

    setLoading(true);
    try {


      const res = await fetchCart();
      console.log("CART DATA:", res.data);

      setCart({
        items: res.data.data.items || []
      });

    } catch (err) {
      if (err.response && (err.response.status === 401 || err.response?.status === 403)) {

        navigate("/login");
      }
    }

    finally {
      setLoading(false);
    }

  };





  useEffect(() => {

    loadCart();




  }, []);


  useEffect(() => {
    const refreshCart = () => {
      loadCart();
    };

    window.addEventListener("cartUpdated", refreshCart);
    return () => {

      window.removeEventListener("cartUpdated", refreshCart);
    };
  }, []);


  const increaseQty = async (productId) => {

    setCartLoading(true);
    try {


      await addToCart(productId)


      loadCart();


      window.dispatchEvent(new Event("cartUpdated"));
    } catch (err) {
      console.log("INCREASE ERROR:", err);

    } finally {
      setCartLoading(false);
    }





  };

  const decreaseQty = async (productId) => {

    setCartLoading(true);

    try {

      await decreaseCartItem(productId);

      loadCart();

      window.dispatchEvent(new Event("cartUpdated"));
    } catch (err) {
      console.log("DECREASE ERROR:", err);

    } finally {
      setCartLoading(false);
    }




  };





  const removeFromCart = async (itemId) => {
    setRemoveLoading(true);
    try {


      await removeCartItem(itemId);


      loadCart();

      // toast.info("Item removed from cart");


      window.dispatchEvent(new Event("cartUpdated"));
    } catch (err) {
      console.log("REMOVE ERROR:", err.response?.data || err);


    } finally {
      setRemoveLoading(false);

    }



    };

    const totalAmount = cart.items?.reduce(
      (total, item) => total + item.product.price * item.quantity,
      0

    );






    if (loading) {
      return (
        <div style={{ padding: "40px", textAlign: "center" }}>
          <h2>Loading Cart...</h2>
        </div>
      )
    }


    return (
      <div style={{ padding: "20px" }}>
        <h2>My Cart</h2>
        {cart.items?.length === 0 && <p>Cart is empty</p>}

        {cart.items?.map((item) => (
          <div key={item.id}
            style={{
              display: "flex",
              justifyContent: "space-between",
              border: "1px solid #ddd",
              padding: "15px",
              borderRadius: "10px",
              marginBottom: "15px",
              background: "#fff"
            }}>


            <div style={{ display: "flex", gap: "15px" }}>
              <img src={item.product.image} alt="" style={{ width: "80px", height: "80px", objectFit: "cover" }} />
              <div>
                <h4>{item.product.name}</h4>
                <p>${item.product.price}</p>
              </div>
            </div>

            <div style={{ textAlign: "right" }}>
              <div style={{ display: "flex", gap: "10px", }}>

                <button onClick={() => decreaseQty(item.product.id)} disabled={cartLoading}>{cartLoading ? "..." : "-"}
                </button>

                <span>{item.quantity}</span>

                <button onClick={() => increaseQty(item.product.id)} disabled={cartLoading}>{cartLoading ? "..." : "+"}
                </button></div>


              <button onClick={() => removeFromCart(item.id)} disabled={removeLoading}
                style={{ color: "red", marginTop: "10px" }}>{removeLoading ? "Removing..." : "Remove"}
              </button>

              <h4>${item.product.price * item.quantity}</h4>

            </div>
          </div>
        ))}








        {cart.items?.length > 0 && (
          <>


            <h3>Total:${totalAmount}</h3>


            <button
              onClick={() => navigate("/checkout")}

              style={{
                padding: "10px 20px",
                background: "green",
                color: "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                marginTop: "10px"

              }}
            >
              Proceed to Checkout
            </button>


          </>
        )}

      </div>

    );
  }

  export default Cart;

