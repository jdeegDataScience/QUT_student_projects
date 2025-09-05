import { useState, useContext } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-material.css";

// import context provider
import { VideosSearchContext } from '../pages/Videos';

/* Components */
import FeatureVideo from "../components/FeatureVideo";
import VideoDetailsButton from "./VideoDetailsButton";
import ErrorAlert from "./ErrorAlert";

export default function VideosTable() {
    const [ searchURL, setSearchURL ] = useContext(VideosSearchContext);
    const [ selectedRow, setSelectedRow ] = useState('');
    const [ error, setError ] = useState(null);
    const columns= [
        {field: "id", valueGetter: "node.data.id", hide: true}, // width: "110px"},
        {field: "title", flex: 2} ,
        {field: "year", flex: 1},
        {field: "classification", flex: 1},
        {field: "IMDB", flex: 1},
        {field: "rottenTomatoes", flex: 1},
        {field: "metacritic", flex: 1}
    ];
    const blockSize = 100;

    const onRowSelected = (e) => {
        if (e.node.isSelected()) {
            setSelectedRow(e.node.data.id);
        }
    };

    const rowSelection =  {
        mode: 'singleRow',
        checkboxes: false,
        enableClickSelection: true
    };

    const getRowId = (params) => params.data.id;
    
    const gridOptions = {
        columnDefs: columns,
        getRowId: getRowId,
        rowBuffer: 2,
        rowModelType: "infinite",
        cacheBlockSize: blockSize,
        cacheOverflowSize: 2,
        maxConcurrentDatasourceRequests: 1,
        infiniteInitialRowCount: 200,
        maxBlocksInCache: 10,
        rowSelection: rowSelection,
        onRowSelected: onRowSelected
    };

    const onGridReady = (params) => {
        let thisTotalVideos = 0;
        const dataSource = {
            rowCount: undefined,
            getRows: (params) => {
                let currPage = Math.floor(params.endRow / blockSize);
                                
                fetch(`${searchURL}&page=${currPage}`)
                .then((res) => res.json())
                .then((results) => {
                    thisTotalVideos = results.pagination.total;
                    
                    return (results.data.map((video) => ({
                        id: video.imdbID,
                        title: video.title,
                        year: video.year,
                        classification: video.classification,
                        IMDB: video.imdbRating,
                        rottenTomatoes: video.rottenTomatoesRating,
                        metacritic: video.metacriticRating 
                        })
                    ));
                })
                .then(newVideos => {
                    if (newVideos?.length) {                        
                        params.successCallback(newVideos, thisTotalVideos);
                        if (params.startRow == 0) {
                            setSelectedRow([newVideos[0].id]);                       
                        }
                    }
                    else params.failCallback();
                })
                .catch((e) => {
                    console.log(e);
                    setError(e.message);
                });
            },
        };
        params.api.setGridOption("datasource", dataSource);
    };

    if (error) { return <ErrorAlert errorState={error} dismissError={() => {setError(null);}} />}
    return (        
        <div className="videos-table-wrapper">
            <div className="video-panel">
                <FeatureVideo videoID={selectedRow} />
                <VideoDetailsButton videoID={selectedRow} />
            </div>
            <div className="ag-theme-material" style={{ height: "100%", width: "100%"}}>
                <AgGridReact key={searchURL} gridOptions={gridOptions} onGridReady={onGridReady}/>
            </div>
        </div>
    )
}


/* useEffect(() => {
    console.log('');
    console.log("VideosTable (Child B)");
    console.log("Child B context state after update: " + searchURL);

    console.log('');
    console.log("VideosTable (Child B) Update A different Var");

    fetch(searchURL)
    .then((res) => res.json())
    .then((data) => { 
        setTotalNumResults(data.pagination.total);
        console.log("Total Videos Returned: " + data.pagination.total); 
    });       
}, [searchURL]); */

/* useEffect(() => { 
    fetch(searchURL)
    .then((res) => res.json())
    .then((data) => {
        if (data.data?.length) {
            setSelectedRow(data.data[0].imdbID);
            console.log("Total Videos Returned: " + data.pagination.total);
        }
    });       
}, [searchURL]); */
