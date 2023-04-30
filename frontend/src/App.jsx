import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState([]);

  const handleFileInputChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a video file');
      return;
    }
    const formData = new FormData();
    formData.append('video', file);
    try {
      console.log("..frontend..")
      const response = await axios.post('http://127.0.0.1:5173/api/classify-scenes', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data.result);
    } catch (error) {
      console.error(error);
    }
  };


  // app.post('/api/classify-scenes', async (req, res) => {
  //   const { videoUrl } = req.body;

  //   try {
  //     const response = await axios.post('http://localhost:5000/api/classify-scenes', { videoUrl });
  //     res.send(response.data);
  //   } catch (error) {
  //     console.error(error);
  //     res.status(500).send('Server Error');
  //   }
  // });



  return (
    <div className="container">
      <h1>Scene Classification</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="video/*" onChange={handleFileInputChange} />
        <button type="submit">Classify Scenes</button>
      </form>
      {result.length > 0 && (
        <div>
          <h2>Results:</h2>
          <ul>
            {result.map((item, index) => (
              <li key={index}>
                {item.class}: {item.frames.join(', ')}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;

// return (
//   <div className="container">
//     <h1>Cricket Scene Classifier</h1>
//     <label htmlFor="video-upload">Select a video to classify scenes:</label>
//     <input type="file" id="video-upload" accept="video/*" onChange={handleVideoUpload} />
//     {thumbnailUrl && <img src={thumbnailUrl} alt="Selected video thumbnail" className="thumbnail" />}
//     <button onClick={handleClassifyScenes} className="classify-button">Classify Scenes</button>
//   </div>
// );