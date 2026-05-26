import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";


import API from "../api";


function PrivateRoute  ({ children }) {
    const [isAuth, setIsAuth] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            try{
                await API.get("/profile/", {
                    withCredentials: true,
                });
                setIsAuth(true);
            }catch (err) {
                setIsAuth(false);

            }
        };
        checkAuth();
    }, []);

    if (isAuth === null) return <div>Loading...</div>;
    if (!isAuth) return <Navigate to="/login"  replace />;



    return children;
}

export default PrivateRoute;

