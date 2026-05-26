import React from "react";

const OrderProgress = ({ status }) => {

   const steps = ["PLACED", "PROCESSING", "PACKED", "SHIPPED", "DELIVERED"];
   const currentIndex = steps.indexOf(status?.toUpperCase());

   return (
     <div style={{ margin: "20px 0" }}>
        <div style={{
            display: "flex",
            alignitems: "center",
            justifyContent: "space-between",
            position: "relative"
        }}
        >
         {steps.map((step, index) => (
           <div key={step} style={{ textAlign: "center", flex: 1 }}>
             {/* Circle */}
             <div style={{
                width: "30px",
                height: "30px",
                borderRadius: "50%",
                margin: "0 auto",
                backgroundColor: index <= currentIndex ? "green" : "#ccc",
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                zIndex: 2,
             }}
            >

               { index < steps.length -1 && (
                  <div 
                     style={{
                        position:"absolute",
                        top:"15px",
                        left:"50%",
                        width:"100%",
                        height:"2px",
                        backgroundColor:
                          index < currentIndex ? "green": "#ccc", zIndex: 1,
                     }}
                     />
               )}
               {index < currentIndex  ? "✅" :index + 1}
                </div>

              {/* Label */}
              <p style={{
                fontSize: "12px",
                marginTop: "5px",
                color: index <= currentIndex ? "green" : "#999",
              }}
            >
                {step}
            </p>
                
         </div>
         ))}

            {/* Background Line */}
             <div style={{
                position: "absolute",
                top: "15px",
                left: "0",
                right: "0",
                height: "4px",
                backgroundColor: "#ccc",
                zIndex: 0,
             }}
          />

          {/* Green Progress Line */}

             <div style={{
                position: "absolute",
                top: "15px",
                left: "0",
                height: "6px",
                width: `${((currentIndex + 1) / steps.length) * 100}%`,
                backgroundColor: "green",
                zIndex: 1,
                transition: "all 0.4s ease",
             }}
            />
            </div>
            </div>
   );
};

export default OrderProgress;


               