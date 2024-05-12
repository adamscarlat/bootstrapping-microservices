const express = require("express");
const path = require("path");
const axios = require("axios");

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