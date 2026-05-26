import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../api";

function AdminRoute({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        API.get("/profile/")
        .then((res) => {
            setUser(res.data);
            setLoading(false);

        })
        .catch(() => {
            setUser(null);
            setLoading(false);
        });
    }, []);

    if (loading) return <div>Loading...</div>;

    
    

  

    if(!user || user.role !== "admin")  {
        return <Navigate to="/"  />;
    }

    return children;
}

export default AdminRoute;