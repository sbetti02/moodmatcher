import React, { useState, useEffect } from 'react';

import SearchBox from './searchbox.js';
import './App.css';

function App() {
  const [tracks, setTracks] = useState([]);

  return (
    <div className="App">
      <p />
      <SearchBox tracks={tracks}
                 setTracks={setTracks}/>
      {tracks.map((track, index) =>
        <li key={ index }>{ track.artists }: { track.title }</li>
      )}

    </div>
  );
}

export default App;
