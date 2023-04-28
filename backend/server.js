import express from 'express';
import multer, { diskStorage } from 'multer';
import ffmpeg from 'ffmpeg';
const app = express();
const port = process.env.PORT || 5000;

const storage = diskStorage({
    destination: function (req, file, cb) {
        cb(null, './uploads');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ storage: storage });

app.post('/classify-scenes', upload.single('video'), (req, res) => {
    const videoPath = req.file.path;
    const outputPath = './uploads/frames';

    try {
        const process = new ffmpeg(videoPath);
        process.then((video) => {
            video.fnExtractFrameToJPG(outputPath, {
                frame_rate: 1,
                number: -1
            }, (error, files) => {
                if (error) {
                    console.error(error);
                    return res.status(500).send('Error extracting frames from video');
                }

                // Call your pre-trained model to classify the frames here

                return res.status(200).send('Scenes classified successfully');
            });
        }, (error) => {
            console.error(error);
            return res.status(500).send('Error processing video');
        });
    } catch (error) {
        console.error(error);
        return res.status(500).send('Error processing video');
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
