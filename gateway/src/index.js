const express = require("express");
const path = require("path");
const axios = require("axios");
var bodyParser = require('body-parser');
var multer = require('multer');
var forms = multer();

if (!process.env.PORT) {
    throw new Error("Please specify the port number for the HTTP server with the environment variable PORT.");
}
const PORT = process.env.PORT;

//
// Starts the microservice.
//
async function startMicroservice(dbhost, dbname) {

    const app = express();

    app.set("views", path.join(__dirname, "views")); // Set directory that contains templates for views.
    app.set("view engine", "hbs"); // Use hbs as the view engine for Express.
    
    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: true }));

    app.use(express.static("public"));

    // Main web page that lists videos.
    app.get("/", async (req, res) => {

        // Retreives the list of videos from the metadata microservice.
        const videosResponse = await axios.get("http://metadata/videos");
        console.log(videosResponse.data)
        // Renders the video list for display in the browser.
        res.render("video-list", { videos: videosResponse.data.videos });
    });
    
    app.get("/video", async (req, res) => {

        const response = await axios({ // Forwards the request to the video-streaming microservice.
            method: "GET",
            url: `http://video-streaming/video?id=${req.query.id}`, 
            data: req, 
            responseType: "stream",
        });

        res.setHeader("Content-Type", "video/mp4")

        response.data.pipe(res);
    });

    // Web page to upload a new video.
    app.get("/upload", (req, res) => {
        res.render("upload-video", {});
    });

    // HTTP POST route to upload video from the user's browser.
    app.post("/api/upload", forms.array("file"), async (req, res) => {
       
        console.log(req.files)
        
        const uint8Array = new Uint8Array(req.files[0].buffer);
        const blob = new Blob([uint8Array], { type: 'application/octet-stream' });

        const url = 'http://azure-storage/upload';
        const formData = new FormData();
        formData.append('file', blob)
        formData.append('fileName', req.files[0].originalname)
        const headers = {
            'content-type': 'multipart/form-data',
        }
        const response = await axios({
            method: "POST",
            url,
            data: formData,
            headers
        })
        response.data.pipe(res);
    });

    // Web page to show the users viewing history.
    app.get("/history", async (req, res) => {

        // Retreives the data from the history microservice.
        const historyResponse = await axios.get("http://history/history");

        // Renders the history for display in the browser.
        res.render("history", { videos: historyResponse.data.history });
    });


	app.listen(PORT, () => {
        console.log("Microservice online at localhost:" + PORT);
    });    
}

//
// Application entry point.
//
async function main() {
    await startMicroservice();
}

main()
    .catch(err => {
        console.error("Microservice failed to start.");
        console.error(err && err.stack || err);
    });