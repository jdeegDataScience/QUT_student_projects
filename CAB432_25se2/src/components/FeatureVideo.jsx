import { useState, useEffect } from "react";

export default function FeatureVideo(props) {
    const videoID = props.videoID;
    const [ videoData, setVideoData ] = useState({title:'', imgURL:null, plot:''});

    const addDefaultImg = ev => {
        ev.target.src = "../public/default_image.jpg";
    }
    
    useEffect(() => {
        if (videoID.length > 0) {
            let video_data_url = `${localStorage.API_URL}/videos/data/${movieID}`;
            fetch(movie_data_url)
            .then((res) => res.json())
            .then((data) => {
                setMovieData({
                    title: data.title,
                    imgURL: data.poster,
                    plot: data.plot
                });
            });
        }
        else {setMovieData({
            title: "Loading search results...",
            imgURL: "../public/loading_image.avif",
            plot: "Please wait for search results to load."
            })
    }}, [movieID])

    return (
        <div className="featured-movie">
            <img src={movieData.imgURL} onError={addDefaultImg}
            alt={ movieData.title + " poster (if available)"} />
            <p className="plot">{movieData.plot}</p>
        </div>
    )
} 