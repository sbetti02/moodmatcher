import React, { useState, useEffect } from 'react';

import './App.css';

function App() {
  const [currentTrack, setCurrentTrack] = useState({});

  useEffect(() => {
    fetch('/70eFcWOvlMObDhURTqT4Fv/info')
      .then(res => res.json())
      .then(data => setCurrentTrack(data));
  }, []);

  return (
    <div className="App">
      <p>Current track: { currentTrack.artists }: { currentTrack.title } </p>
    </div>
  );
}

export default App;
