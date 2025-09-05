import { Link, useNavigate } from "react-router-dom";
import React, { useState, useContext, useEffect } from "react";

// import context provider
import { AuthContext } from '../App';

// navigation links
export default function Header() {
    const [authenticated, setAuthenticated] = useContext(AuthContext);
    const url = `${localStorage.API_URL}/user/logout`
    const [ userEmail, setUserEmail ] = useState(localStorage.getItem("userEmail"));

    useEffect(() => { 
        setUserEmail(localStorage.getItem("userEmail"))}, [authenticated]
    );
 
    const Logout = () => {
        const currToken = localStorage.getItem("refreshToken");
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json" ,
                "accept": "application/json"
            },
            body: JSON.stringify({ refreshToken: currToken }),
        })
        .finally(() => {
            setAuthenticated(false);
        });
    }

    return (
        <nav id={authenticated.toString()}>
            <ul className="left-side">
                <li><Link to="/">Home</Link></li>
				{
                    authenticated ? 
                    <li><Link to="/videos">Videos</Link></li>
                    : null
                }
            </ul>
            <ul className="right-side">
                {
                    authenticated ? 
                    <li className="sessionUserEmail">{userEmail}</li> 
                    : null
                }
                {
                    authenticated ? 
                    <li><button type="button" onClick={Logout}>Logout</button></li> 
                    : <li><Link to="/login">Login</Link></li>
                }
            </ul>
        </nav>
    );
}