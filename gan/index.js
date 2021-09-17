const express = require("express");
const cors = require("cors");
const path = require("path");
const multer = require("multer");
const app = express();
const serverPort = 6060;

//#region Setup
app.use(cors());

const dir = path.join(__dirname, "public");
app.use(express.static(dir));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

//#region User Data Sets Storage
const userDataSetsStorage = multer.diskStorage({
  destination: function (_, _, cb) {
    cb(null, "public/userdatasets");
  },
  filename: function (_, file, cb) {
    cb(null, file.originalname);
  },
});
const uploadUserDataSets = multer({ storage: userDataSetsStorage }).single("file");
//#endregion

//#region Image Data Sets Storage
const ImageDataSetsStorage = multer.diskStorage({
    destination: function (_, _, cb) {
      cb(null, "public/userdatasets");
    },
    filename: function (_, file, cb) {
      cb(null, file.originalname);
    },
  });
const uploadImageDataSets = multer({ storage: ImageDataSetsStorage }).single("file");
//#endregion

//#endregion

app.post("/upload-data-sets", (req, res) => {
    console.log("Request: Upload Data Sets");
    uploadUserDataSets(req, res, (err) => {
        if (err instanceof multer.MulterError || err) {
            return res.status(500).json(err);
        }
        res.status(200).send("File is uploaded successfully.");
    });
});

app.post("/upload-image-data-sets", (req, res) => {
    console.log("Request: Upload Image Data Sets");
    uploadImageDataSets(req, res, (err) => {
        if (err instanceof multer.MulterError || err) {
            return res.status(500).json(err);
        }
        res.status(200).send("File is uploaded successfully.");
    });
});

app.get("/generate-image-from-user-data-sets", (req, res) => {
    console.log("Request: Generate Image From User Data Sets");
    res.status(200).send("Generated an image from user data sets.");
});

app.get("/generate-image", (req, res) => {
    console.log("Request: Generate Image");
    res.status(200).send("Generated an image.");
});

app.listen(serverPort, () => {
    console.log(`Server is running at ${serverPort}`);
});