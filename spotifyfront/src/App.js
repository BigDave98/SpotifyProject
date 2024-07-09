import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSongs, setSelectedSongs] = useState(new Set());

  const fetchData = (page) => {
  fetch(`/get_all_tracks?page=${page}&search=${searchTerm}`)
    .then(res => res.json())
    .then(data => {
      setData(data.tracks);
      setTotalPages(data.total_pages);
      setCurrentPage(data.current_page);
      console.log(data);
    })
    .catch(error => console.error('Error fetching data:', error));
};

  useEffect(() => {
    fetchData(currentPage);
  }, [currentPage, searchTerm]);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1); // Reset page to 1 when performing a new search
    return event.target.value
  };

  const handleCheckboxChange = (event) => {
      const song = event.target.value;
      if (event.target.checked) {
        setSelectedSongs((prevSelected) => new Set([...prevSelected, song]));
      } else {
        setSelectedSongs((prevSelected) => {
          const newSelected = new Set(prevSelected);
          newSelected.delete(song);
          return newSelected;
        });
      }
};

  const handleSubmitSelectedSongs = () => {
    console.log(Array.from(selectedSongs)); // Array dos songs selecionados

    fetch('/submit_selected_songs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ selectedSongs: Array.from(selectedSongs) }),
    })
      .then(res => res.json())
      .then(data => {
        console.log('Response from server:', data);
      })
      .catch(error => console.error('Error submitting selected songs:', error));
  };

  return (
    <div>
      <h1>Liked Songs</h1>
      <input
          type="text"
          id="search"
          placeholder="Search by Music name or Author"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
      />
      <table>
        <thead>
          <tr>
            <th>Select</th>
            <th>Music Name - Author</th>
          </tr>
        </thead>
        <tbody id="music-list">
          {data.map((song, index) => (
            <tr key={index}>
              <td>
                <input
                  type="checkbox"
                  className="song-checkbox"
                  value={song}
                  onChange={handleCheckboxChange}
                />
              </td>
              <td>{song}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="pagination">
        <button onClick={handlePreviousPage} disabled={currentPage === 1}>
          Previous
        </button>
        <span>{`Page ${currentPage} of ${totalPages}`}</span>
        <button onClick={handleNextPage} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
      <div className="actions">
        <button id="submit-btn" onClick={handleSubmitSelectedSongs}>
          Submit Selected Songs
        </button>
      </div>
    </div>
  );
}

export default App;
