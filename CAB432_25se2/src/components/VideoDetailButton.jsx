import React from "react";

import { useNavigate  } from 'react-router-dom';

export default function VideoDetailsButton(props) {
    const videoID = props.videoID;
    const navigate = useNavigate();

    const handleClick = (event) => {
        event.preventDefault();
        navigate(`/videoDetails/${event.target.value}`)
    };

    return (
        <div className="submit-container" aria-labelledby="video-data-button">
            <button type="button" id="video-data-button" 
            value={videoID} onClick={handleClick}>
            Details...
            </button>
        </div>
    )
}