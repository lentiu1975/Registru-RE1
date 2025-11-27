import React, { useState, useEffect, useRef } from 'react';
import { manifestAPI, yearsAPI, authAPI, latestManifestAPI } from '../services/api';
import './Search.css';

function Search({ onLogout }) {
  const [years, setYears] = useState([]);
  const [selectedYear, setSelectedYear] = useState('');
  const [container, setContainer] = useState('');
  const [results, setResults] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [latestManifest, setLatestManifest] = useState(null);
  const containerInputRef = useRef(null);

  // Încarcă anii disponibili la montare
  useEffect(() => {
    loadYears();
  }, []);

  // Încarcă ultimul manifest când se schimbă anul
  useEffect(() => {
    if (selectedYear) {
      loadLatestManifest();
    }
  }, [selectedYear]);

  const loadYears = async () => {
    try {
      const data = await yearsAPI.getAll();
      setYears(data);
      // Setează anul activ implicit
      const activeYear = data.find(y => y.is_active);
      if (activeYear) {
        setSelectedYear(activeYear.year);
      } else if (data.length > 0) {
        setSelectedYear(data[0].year);
      }
    } catch (err) {
      console.error('Error loading years:', err);
    }
  };

  const loadLatestManifest = async () => {
    try {
      const data = await latestManifestAPI.get(selectedYear);
      setLatestManifest(data);
    } catch (err) {
      console.error('Error loading latest manifest:', err);
      setLatestManifest(null);
    }
  };

  const validateContainer = (value) => {
    // Extrage doar cifrele din container
    const digits = value.replace(/\D/g, '');
    return digits.length >= 7;
  };

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!container.trim()) {
      setError('Vă rugăm să introduceți numărul containerului');
      return;
    }

    if (!validateContainer(container)) {
      setError('Containerul trebuie să conțină minim 7 cifre');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const searchParams = {
        container: container.trim(),
        year: selectedYear
      };

      const data = await manifestAPI.search(searchParams);

      if (data && data.length > 0) {
        setResults(data);
        setCurrentIndex(0);
        setContainer(''); // Golește câmpul de căutare după căutare reușită
        // Setează focusul înapoi pe câmpul de căutare
        setTimeout(() => {
          containerInputRef.current?.focus();
        }, 100);
      } else {
        setResults([]);
        setError('Nu au fost găsite rezultate');
      }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Eroare la căutare. Vă rugăm să încercați din nou.');
      }
      console.error('Search error:', err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < results.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
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

  const handleHome = () => {
    // Șterge rezultatele și resetează formularul
    setResults([]);
    setCurrentIndex(0);
    setContainer('');
    setError('');
  };

  const currentResult = results.length > 0 ? results[currentIndex] : null;

  return (
    <div className="search-container">
      <header className="search-header">
        <div className="header-content">
          <h1>Registru import RE1 {selectedYear}</h1>
          <button onClick={handleLogout} className="logout-button">
            Deconectare
          </button>
        </div>
      </header>

      <div className="search-content">
        {/* Ultimul manifest actualizat */}
        {latestManifest && latestManifest.numar_manifest && (
          <div className="latest-manifest-wrapper">
            <button onClick={handleHome} className="home-button" title="Înapoi la pagina principală">
              🏠 Acasă
            </button>
            <div className="latest-manifest-info">
              Ultimul navă actualizată: <strong>{latestManifest.nume_nava || 'N/A'}</strong>, manifest <strong>{latestManifest.numar_manifest}</strong> din data <strong>{latestManifest.data_inregistrare}</strong>
            </div>
          </div>
        )}

        {/* Secțiune căutare */}
        <div className="search-section">
          <form onSubmit={handleSearch} className="search-form">
            <div className="form-row-horizontal">
              <div className="form-group year-select">
                <label htmlFor="year">An:</label>
                <select
                  id="year"
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(e.target.value)}
                  className="year-dropdown"
                >
                  {years.map(year => (
                    <option key={year.id} value={year.year}>
                      {year.year} {year.is_active ? '(Activ)' : ''}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group container-search">
                <label htmlFor="container">Căutare Container (minim 7 cifre):</label>
                <input
                  type="text"
                  id="container"
                  ref={containerInputRef}
                  value={container}
                  onChange={(e) => setContainer(e.target.value)}
                  placeholder="Ex: ABCD1234567"
                  className="container-input"
                />
              </div>

              <button type="submit" className="search-button" disabled={loading}>
                {loading ? 'Se caută...' : 'Căutare'}
              </button>
            </div>
          </form>

          {error && <div className="error-message">{error}</div>}

          {/* Bara de navigare rezultate */}
          {results.length > 0 && (
            <div className="results-navigation">
              <span className="results-count">
                Rezultate găsite: {results.length}
              </span>
              {results.length > 1 && (
                <div className="navigation-buttons">
                  <button
                    onClick={handlePrevious}
                    disabled={currentIndex === 0}
                    className="nav-button"
                  >
                    ◀ Anterior
                  </button>
                  <span className="current-position">
                    {currentIndex + 1} / {results.length}
                  </span>
                  <button
                    onClick={handleNext}
                    disabled={currentIndex === results.length - 1}
                    className="nav-button"
                  >
                    Următor ▶
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Secțiune rezultate - Layout Split */}
        {currentResult && (
          <div className="results-section">
            <div className="result-details">
              {/* Partea stângă - Informații text */}
              <div className="details-left">
                <div className="position-title">
                  Poziție RE1
                </div>

                <div className="manifest-info">
                  {currentResult.numar_manifest}/{currentResult.numar_permis}/{currentResult.numar_pozitie}/{currentResult.cerere_operatiune} – {currentResult.data_inregistrare_formatted || currentResult.data_inregistrare}
                </div>

                <div className="info-item info-row">
                  <div className="info-col">
                    <span className="info-label">Colete:</span>
                    <span className="info-value">{currentResult.numar_colete || 'N/A'}</span>
                  </div>
                  <div className="info-col">
                    <span className="info-label">Greutate:</span>
                    <span className="info-value">{currentResult.greutate_bruta ? `${currentResult.greutate_bruta} Kg` : 'N/A'}</span>
                  </div>
                </div>

                <div className="info-item">
                  <span className="info-label">Tip operațiune:</span>
                  <span className="info-value">
                    {currentResult.tip_operatiune === 'I' ? 'Import' :
                     currentResult.tip_operatiune === 'T' ? 'Transhipment' :
                     currentResult.tip_operatiune || 'N/A'}
                  </span>
                </div>

                <div className="info-item description">
                  <span className="info-label">Descriere marfă:</span>
                  <div className="info-value">{currentResult.descriere_marfa || 'N/A'}</div>
                </div>

                <div className="info-item">
                  <span className="info-label">Număr sumară:</span>
                  <span className="info-value">
                    {currentResult.numar_sumara ? (
                      currentResult.numar_sumara.includes(';') || currentResult.numar_sumara.includes(',') ? (
                        currentResult.numar_sumara.split(/[;,]/).map((item, index) => (
                          <div key={index}>{item.trim()}</div>
                        ))
                      ) : (
                        currentResult.numar_sumara
                      )
                    ) : (
                      'N/A'
                    )}
                  </span>
                </div>
              </div>

              {/* Partea dreaptă - Imagini */}
              <div className="details-right">
                {/* Secțiune Container */}
                <div className="container-section">
                  <div className="container-title">{currentResult.container || 'Container necunoscut'}</div>
                  <img
                    src={currentResult.container_type_data?.imagine_url || 'http://localhost:8000/media/container_types/Container.png'}
                    alt="Container"
                    className="container-image-large"
                    onError={(e) => {
                      e.target.src = 'http://localhost:8000/media/container_types/Container.png';
                    }}
                  />
                </div>

                {/* Secțiune Navă */}
                <div className="ship-section">
                  <div className="ship-header">
                    <div className="ship-name">{currentResult.nume_nava || 'Nava nedefinită'}</div>
                    {currentResult.ship_data && currentResult.ship_data.pavilion_data && currentResult.ship_data.pavilion_data.imagine_url && (
                      <img
                        src={currentResult.ship_data.pavilion_data.imagine_url}
                        alt="Pavilion"
                        title={currentResult.ship_data.pavilion_data.nume_tara || currentResult.ship_data.pavilion_data.nume}
                        className="flag-image-inline"
                      />
                    )}
                  </div>

                  {currentResult.ship_data && currentResult.ship_data.imagine_url && (
                    <img
                      src={currentResult.ship_data.imagine_url}
                      alt="Navă"
                      className="ship-image"
                    />
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Search;
