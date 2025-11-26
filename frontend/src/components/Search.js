import React, { useState } from 'react';
import { manifestAPI, authAPI } from '../services/api';
import ResultsTable from './ResultsTable';
import './Search.css';

function Search({ onLogout }) {
  const [container, setContainer] = useState('');
  const [numarManifest, setNumarManifest] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!container && !numarManifest) {
      setError('Vă rugăm să introduceți cel puțin un criteriu de căutare');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const searchParams = {};
      if (container) searchParams.container = container;
      if (numarManifest) searchParams.numar_manifest = numarManifest;

      const data = await manifestAPI.search(searchParams);
      setResults(data);
    } catch (err) {
      setError('Eroare la căutare. Vă rugăm să încercați din nou.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setContainer('');
    setNumarManifest('');
    setResults(null);
    setError('');
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      onLogout();
    } catch (err) {
      console.error('Logout error:', err);
      onLogout();
    }
  };

  return (
    <div className="search-container">
      <header className="search-header">
        <div className="header-content">
          <h1>Registru Import 2025</h1>
          <button onClick={handleLogout} className="logout-button">
            Deconectare
          </button>
        </div>
      </header>

      <div className="search-content">
        <div className="search-box">
          <h2>Căutare Manifest</h2>

          <form onSubmit={handleSearch} className="search-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="container">Container</label>
                <input
                  type="text"
                  id="container"
                  value={container}
                  onChange={(e) => setContainer(e.target.value)}
                  placeholder="Introduceți numărul containerului"
                />
              </div>

              <div className="form-group">
                <label htmlFor="numarManifest">Număr Manifest</label>
                <input
                  type="text"
                  id="numarManifest"
                  value={numarManifest}
                  onChange={(e) => setNumarManifest(e.target.value)}
                  placeholder="Introduceți numărul manifestului"
                />
              </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="button-group">
              <button type="submit" className="search-button" disabled={loading}>
                {loading ? 'Se caută...' : 'Căutare'}
              </button>
              <button type="button" onClick={handleClear} className="clear-button">
                Resetare
              </button>
            </div>
          </form>
        </div>

        {results && <ResultsTable results={results} />}
      </div>
    </div>
  );
}

export default Search;
