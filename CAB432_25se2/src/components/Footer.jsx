import { useNavigate } from "react-router-dom";

export default function Footer() {
    const navigate = useNavigate();
    return (
        <nav className="footer">
            <ul className="right-side">
                <li><button type="button" onClick={() => {navigate(-1);}}>Back</button></li>
            </ul>
        </nav>
    )
}