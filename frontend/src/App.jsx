import './App.css'
import React, { useState } from 'react';


function App() {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [thumbnailUrl, setThumbnailUrl] = useState(null);

  const handleVideoUpload = (event) => {
    const file = event.target.files[0];
    setSelectedVideo(file);
    setThumbnailUrl(URL.createObjectURL(file));
  };

  const handleClassifyScenes = () => {
    // Send the selectedVideo to the backend to classify scenes
  };

  return (
    <div className="container">
      <h1>Cricket Scene Classifier</h1>
      <label htmlFor="video-upload">Select a video to classify scenes:</label>
      <input type="file" id="video-upload" accept="video/*" onChange={handleVideoUpload} />
      {thumbnailUrl && <img src={thumbnailUrl} alt="Selected video thumbnail" className="thumbnail" />}
      <button onClick={handleClassifyScenes} className="classify-button">Classify Scenes</button>
    </div>
  );
}

export default App;