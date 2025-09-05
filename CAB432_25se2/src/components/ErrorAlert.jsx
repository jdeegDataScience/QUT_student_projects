import React from "react";

export default function ErrorAlert({errorState, dismissError}) {
    const error = errorState?.message;

    if (!error) { return null;}

    return (
        <div className="alert" aria-labelledby="error">
            {/* <img src="../spidey-senses-icon.jpg" alt="icon of spiderman's spidersenses activating"/> */}
            <div className="alert-content">
                <h2>My error-senses are tingling...</h2>
                <p id="error">Error: {error}</p>
                <button type="button" id="error-button" onClick={dismissError} aria-label="dismiss error">
                Dismiss
                </button>
            </div>
        </div>
    )
}