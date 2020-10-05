import React, { useState, useEffect } from 'react';


function SearchBox(props) {
    const [search, setInput] = useState('');

    const handleSearch = (e) => {
        e.preventDefault();
        fetch(`/${search}/info`)
            .then(res => res.json())
            .then(data => {
                if ('title' in data) {
                    props.setTracks(props.tracks.concat(data));
                }
                else {
                    alert(`${data.status} - ${data.message}`)
                }


            });
    }

    return (
        <>
            <form onSubmit={handleSearch}>
                <label>
                    Track ID:
                    <input type="text"
                           value={search}
                           onChange={e => setInput(e.target.value)}
                           size='30'
                    />
                </label>
                <input type="submit" value="Submit" />
            </form>
        </>
    );
}

export default SearchBox;
