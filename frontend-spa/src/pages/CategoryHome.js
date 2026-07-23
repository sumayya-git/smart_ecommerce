import React, { useEffect, useState }  from "react";

import { useNavigate } from "react-router-dom";
import API from "../api";


function CategoryHome() {

    const [categories, setCategories] = useState([]);
    const [hoveredId, setHoveredId] = useState(null);

   
    const navigate = useNavigate();


    //🔥fetch products from backend

    useEffect(() => {
      const fetchCategories = async () => {
        try{
          const res = await API.get("categories/");

          
          setCategories(res.data);

          console.log(res.data);
       
        } catch (err) {

           console.log("Error fetching categories:",err);
        }
      };

      fetchCategories();
    }, []);
    


    

    const parentCategories = categories.filter((cat) => cat.parent === null);

 
   
    return (
       
        <div style={{ padding:"20px", backgroundColor: "#f5f5f5" }}>

            <h2 style={{ marginBottom:"20px"}}>Best Deals</h2>

             <div style={{
                                display:"flex",
                                
                                gap:"20px",
                                flexWrap:"wrap"
                              }}>
            
           

                {parentCategories.map((parent) => (
                    <div key={parent.id} 
                        

                         style={{
                          width:"300px",
                          backgroundColor:"white",
                          padding:"15px",
                          borderRadius:"10px",
                          boxShadow:"0 2px 8px rgba(0,0,0,0.1)"
                              
                            }}>

                              <h3
                                  style={{
                                    color: "#212121",
                                    fontWeight: "bold",
                                    marginBottom: "15px",
                                  }}
                                >
                                  {parent.name}
                                </h3>

                              <div style={{
                                display:"grid",
                                gridTemplateColumns:"1fr 1fr",
                                gap:"10px"
                              }}>

                        {categories
                          .filter(sub => sub.parent === parent.id)
                           .map(sub => {
                              console.log(sub.image);
                              return(
                            

                                                                      <div
                                        key={sub.id}
                                        onClick={() => navigate(`/category/${sub.id}`)}
                                        onMouseEnter={() => setHoveredId(sub.id)}
                                        onMouseLeave={() => setHoveredId(null)}
                                        style={{
                                          cursor: "pointer",
                                          textAlign: "center",
                                          transform:
                                            hoveredId === sub.id ? "translateY(-5px)" : "translateY(0)",
                                          transition: "all 0.3s ease",
                                        }}
                                      >

                                     
                                      <img src={sub.image}
                                        alt={sub.name}
                                       style={{
                                        width:"100%",
                                        height:"100px",
                                        objectFit:"cover",
                                        
                                        borderRadius:"5px",
                                      
                                      }}
                                      />

                                      
                                      
                                        
                                          
                                            <p
                                              style={{
                                                color: "#212121",
                                                fontWeight: "bold",
                                                marginTop: "8px",
                                                marginBottom: "0",
                                              }}
                                            >
                                              {sub.name}
                                            </p>
                                            </div>
                              );
                            })}
                              </div>
                              </div>
                              

                              ))}

                              </div>
                              </div>

                                      
                    
                    
        );
    }

                    
           
export default CategoryHome;