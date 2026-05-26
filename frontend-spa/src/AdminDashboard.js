import { useEffect, useState } from "react";
import { Bar,Pie } from "react-chartjs-2";
import {Line} from "react-chartjs-2";
import API from "./api";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
  
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);



function AdminDashboard() {
    console.log("API import:",API);
    

    const [stats, setStats] = useState(null);
    const [monthly, setMonthly] = useState(null);
    const [topProducts, setTopProducts] = useState([]);
    const [weeklyRevenue, setWeeklyRevenue] = useState([]);
    const [days, setDays] = useState(7);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const stateRes = await API.get("/admin/dashboard/");
                setStats(stateRes.data);

                const monthlyRes = await API.get("/admin/monthly-report/");
                setMonthly(monthlyRes.data);

                 const topProductsRes = await API.get("/admin/top-products/");
                setTopProducts(topProductsRes.data.top_products || []);

                 const revenueRes = await API.get(`/admin/revenue/?days=${days}/`);
                setWeeklyRevenue(revenueRes.data);

            } catch (err) {
                console.log(err);

                if(err.response?.status === 401) {
                    alert("Login required");

                } else if (err.response?.status === 403) {
                    alert("Admin only access ❌");
                }
            }
        };

        fetchData();
    },[days]);



const chartData = {
    labels: ["Total Orders", "Total Users"],
    datasets: [
        {
            label: "Orders & Users",
            data:
              [stats?.total_orders || 0, stats?.total_users || 0],
              
            backgroundColor: ["#4CAF50", "#2196F3"],
        },
     
    
    ],
};

const revenueChartData = {
    labels: ["Total Revenue"],
    datasets: [
        {
            label: "Revenue",
            data: [stats?.total_revenue || 0],
            backgroundColor: ["#FF9800"],
        },
    ]
};

const orderStatusData = {
    labels: ["Shipped", "Cancelled", "Pending"],
    datasets: [
        {
            label: "Order Status",
            data:
             [
                stats?.shipped_orders || 0,
                stats?.cancelled_orders || 0,
                stats?.pending_orders || 0,
             ],
            
           backgroundColor: ["#4CAF50", "#F44336", "#FFC107"],
        },
    ],
};

const weeklyRevenueData = {

    labels: Array.isArray(weeklyRevenue)
     ?weeklyRevenue.map(item => item.data):[],
    datasets: [
        {
            label: "Last 7 Days Revenue",
            data: Array.isArray(weeklyRevenue)
             ?weeklyRevenue.map(item => item.revenue):[],
            borderColor: "#2196F3",
            backgroundColor: "rfba(33,150,243,0.2)",
            tension: 0.4,

        },
    ]
};

const cardStyle = {
    background: "#ffffff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0,1)",
    textAlign: "center",
};

const chartBox = {
    background: "#ffffff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 4px 12px rgba(0,0,0,0,1)",
    
};



return (
  <div style= {{ padding: "30px", fontFamily: "Arial" }}>
    <h2 style={{ marginBottom: "30px" }}>Admin Dashboard</h2>
    

   
       {/* Stats Cards */}
        <div 
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "20px",
            marginBottom: "40px",
          }}
        >
        <div style={cardStyle}>
            <h4>Total Orders</h4>
            <h2>{stats?.total_orders || 0}</h2>
        </div>

        <div style={cardStyle}>
            <h4>Total Users</h4>
            <h2>{stats?.total_users || 0}</h2>
        </div>

         <div style={cardStyle}>
            <h4>Total Revenue</h4>
            <h2>${stats?.total_revenue || 0}</h2>
        </div>

            
   </div>

    {/* Charts */}

    <div style={{ marginBottom: "20px" }}>
        <button onClick={() => setDays(7)}>Last 7 Days</button>
        <button onClick={() => setDays(30)}>Last 30 Days</button>
        <button onClick={() => setDays(90)}>Last 90 Days</button>
    </div>
        <div 
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, 1fr)",
            gap: "40px",
        }}
        >
        <div style={chartBox}>
           <Bar data={chartData} />
        </div>

        <div style={chartBox}>
           <Bar key="bar1" data={revenueChartData} />
        </div>

        <div style={chartBox}>
           <Pie key="pie1" data={orderStatusData} />
        </div>

        <div style={chartBox}>
           <Line key={JSON.stringify(weeklyRevenue)}
                data={weeklyRevenueData}/>
        </div>
     </div>
    
    

    {/* Monthly */}

    {monthly && (
        <div style={{ marginBottom: "30px"}}>
            <h3>Last 30 Days</h3>
            <p>Revenue:${monthly.monthly_revenue}</p>
            <p>Orders Count: {monthly.orders_count}</p>
           
    
        </div>
)}
        {/* Top Products */}
        <div>
            <h3>Top Products</h3>

        <table border="1" cellPadding="10" style={{ borderCollapse: "collapse" }}>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Revenue</th>
                    <th>Stock</th>
                
                </tr>
            </thead>
        <tbody>
          {Array.isArray(topProducts) && 
            topProducts.map((product) => (
                <tr key={product.id}>

                
        
                    <td>{product.name}</td>
                    <td>${product.total_revenue}</td>
                    <td style={{ color: product.stock <= 5 ? "red": "black"}}>
                        {product.stock}
                    </td>
                  </tr>
            ))}
            </tbody>
            </table>


        </div>
        
      
          
      </div>
     
    
 );
}




export default AdminDashboard;