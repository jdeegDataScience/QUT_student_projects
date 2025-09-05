import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import React,{ createContext, useEffect, useState } from 'react';

/* Pages */
import Home from "./pages/Home"
import Login from "./pages/Login";
import Videos from './pages/Videos';
import VideoDetails from './pages/VideoDetails';

// context for user authentication
export const AuthContext = createContext();

/* Components */
import Header from "./components/Header";
import ErrorAlert from "./components/ErrorAlert";
import Footer from './components/Footer';

/*  Hooks */
// import useRefreshToken from './hooks/useRefreshToken';


function App() {
    localStorage.setItem("API_URL", `http://4.237.58.241:3000`);
    const [authenticated, setAuthenticated] = useState(false);
    const [ isTokensRefreshed, loading, refreshError ] = useRefreshToken();
    const [error, setError] = useState();
    

    function changeAuthenticated(value) {
        setAuthenticated(value);
        if (value === false) {
            localStorage.removeItem("bearerToken");
            localStorage.removeItem("refreshToken");
            localStorage.removeItem("userEmail");
        }
    }

    useEffect(() => {
        if (refreshError) {
            setError(refreshError);
            changeAuthenticated(false);  
        }
        else if (isTokensRefreshed) {
            changeAuthenticated(true);
            setError(null);
        }
    }, [loading]);

    return (
        <AuthContext.Provider value={[authenticated, changeAuthenticated]}>
            <BrowserRouter>
                <div className="App">
                    <Header />
                    <ErrorAlert errorState={error} dismissError={() => {setError(null);}} />
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/Videos" element={<Videos />} />
                        <Route path="/VideoDetails/:videoID" element={<VideoDetails />} />
                        <Route path="/Login" element={<Login />} />
                    </Routes>
                    <Footer />
                </div>
            </BrowserRouter>
        </AuthContext.Provider>
    );
}

export default App
