const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const cors = require('cors');
const bodyParser = require('body-parser')

const app = express();
const port = process.env.PORT || 3000;
const upload = multer();
// import bodyParser from 'body-parser'
app.use(bodyParser.json({ extended: true }));
app.use(bodyParser.urlencoded({ extended: true }));

//cors resolving
app.use(cors());

// Endpoint to handle file upload
app.post('/api/classify-scenes', (req, res) => {
  console.log("....")
  // const videoPath = req.files.video.path;

  // Spawn a child process to run the scene_classification.py script
  const py = spawn('python', ['scene_classification.py', req.file.path]);

  let output = '';

  py.stdout.on('data', (data) => {
    output += data.toString();
  });

  py.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });

  py.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python script exited with code ${code}`);
      return res.status(500).send('Internal Server Error');
    }

    // Parse the output from the Python script
    const frames = output.trim().split('\n').map((line) => {
      const [framePath, label] = line.split(',');
      return { framePath, label };
    });

    res.send(frames);
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});