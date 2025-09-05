import { useState, useEffect } from "react";

export default function useRefreshToken() {
    const [ isRefreshSuccess, setIsRefreshSuccess ] = useState(false);
    const [ loading, setLoading ] = useState(true);
    const [ error, setError ] = useState(false);
    const url = `${localStorage.API_URL}/user/refresh`;
    const [ currToken, setCurrToken ] = useState(localStorage.getItem("refreshToken"));

    useEffect(() => {
        if (Boolean(currToken)) {
            fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json" ,
                "accept": "application/json"
            },
            body: JSON.stringify({ refreshToken: currToken }),
            })
            .then((res) => {
                if (res.ok) { return res.json() }
                else {throw new Error("Credentials have expired, please login to refresh your session.");}
            })
            .then((data) => {                
                localStorage.setItem("bearerToken", data.bearerToken.token);
                localStorage.setItem("refreshToken", data.refreshToken.token);
                setIsRefreshSuccess(true);
            })
            .catch((e) => {
                setError(e);
                setCurrToken(null);
            })
            .finally(() => {setLoading(false);})
        };

    }, [])

    return [ isRefreshSuccess, loading, error ];
}