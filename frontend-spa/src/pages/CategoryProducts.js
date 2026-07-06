import { useEffect, useState } from "react";
import  { useParams, useNavigate } from "react-router-dom";


import API from "../api";


function CategoryProducts() {

  const { category } = useParams();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true)
  const [categoryName, setCategoryName] = useState("");

  

  const [next, setNext] = useState(null);
  const [previous, setPrevious] = useState(null);



  const navigate = useNavigate();

  const fetchCategoryName = async () => {
    try {
      const res = await API.get("/categories/");
      const cat = res.data.find( c => String(c.id) ===  String(category));

      if (cat) {
        setCategoryName(cat.name);
      }
    } catch (err) {
      console.log("Error fetching category name");
    }
  };
   

    
    
   
   const fetchProducts = async (
    url = `/products/?category=${category}`
) => {

    setLoading(true);

    try {

        const res = await API.get(url);

        setProducts(res.data.results);
        setNext(res.data.next);
        setPrevious(res.data.previous);

    } catch (err) {

        console.log("Error fetching products:", err);

    }

    setLoading(false);
};

    useEffect(() => {

    fetchProducts();
    fetchCategoryName();

}, [category]);
         
      

     

     const addToCart = async (id) => {
     try{
      await API.post(`/cart/add/${id}/`,{
        quantity: 1
      });
    
          
        
           
          
        
       

        alert("Added to cart ✅");

        window.dispatchEvent(new Event("cartUpdated"));
    }catch (err) {
      console.log(err);
      console.log(err.response);
      console.log(err.response?.data);

      if(err.response?.status === 401) {

      
      
         alert("Please Login first❌");
         navigate("/login");
    }
  }
  };

        
     
  

    
    if(loading) {
      return (
        <div style={{padding:"20px"}}>
          <h2>Loading products...</h2>
        </div>
      )
    }

    return (
        <div style={{ padding: "20px" }}>
           
            <h2>{categoryName}({products.length} items) </h2>
            

            
                {products.length === 0 ? (
                    
                        
                          <p>No products found 😔</p>
                          
                    
                    
                ):(

                 <div style ={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(200px, 1fr))",gap:"20px",}}>
                    {products.map(product => (
                   
                      <div key={product.id}
                        onClick={() => navigate(`/product/${product.id}`)} style={{
                        border:"1px solid #ddd",
                        borderRadius:"10px",
                        padding:"10px",
                        background:"white",
                        
                        
                        cursor:"pointer",
                       
                    }}>
                     
                        <img src={product.image.replace("https://smart-ecommerce-backend.onrender.com","http://127.0.0.1:8000")}alt={product.name} 
                         style={{ width:"100%", height:"150px", objectFit:"contain"}} />
                       
                       
                        <p style={{ fontWeight:"bold" }}>{product.name}</p>
                        <p style={{ color:"green"}}>${product.price}</p>

                        <p style={{
                            color: product.stock === 0 ? "red" : product.stock <= 5 ? "orange" :"green",
                            fontWeight:"bold",
                            
                        }}>
                            {product.stock === 0
                              ? "Out of stock ❌"
                              : product.stock <=5
                              ? `Only ${product.stock} left in stock ⚠️`
                              : "In stock ✅"}
                        </p>

                         <button onClick={(e) => { 
                                e.stopPropagation();
                                addToCart(product.id);
                                    
                              }}
                                disabled={product.stock === 0}
                                style={{
                                  
                                  background: product.stock ===0 ? "#ccc":
                                  "#007bff",
                                  color:"white",
                                  padding:"8px 12px",
                                  
                                  border:"none",
                                  borderRadius:"5px",
                                  cursor: product.stock === 0 ? "not-allowed" :"pointer",
                              }}
                              
                          
                                  
                              
                              >
                                {product.stock === 0 ? "Out of Stock" : "Add to Cart"}
                              </button>
                        </div>

                        
                ))}

            </div>
              )}
                  <div
              style={{
                  marginTop: "20px",
                  display: "flex",
                  justifyContent: "center",
                  gap: "10px",
              }}
          >
              <button
                  disabled={!previous}
                  onClick={() => fetchProducts(previous)}
              >
                  Previous
              </button>

              <button
                  disabled={!next}
                  onClick={() => fetchProducts(next)}
              >
                  Next
              </button>
          </div>
              
        </div>

        
    );
}

export default CategoryProducts;