import React from 'react';
import './ResultsTable.css';

function ResultsTable({ results }) {
  if (!results || !results.results || results.results.length === 0) {
    return (
      <div className="no-results">
        <p>Nu s-au găsit rezultate pentru căutarea dvs.</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('ro-RO', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatNumber = (number) => {
    if (number === null || number === undefined) return '-';
    return number.toString();
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h3>Rezultate căutare</h3>
        <span className="results-count">
          {results.count} {results.count === 1 ? 'rezultat găsit' : 'rezultate găsite'}
        </span>
      </div>

      <div className="table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>Nr. Crt.</th>
              <th>Număr Manifest</th>
              <th>Număr Permis</th>
              <th>Număr Poziție</th>
              <th>Cerere Operațiune</th>
              <th>Data Înregistrare</th>
              <th>Container</th>
              <th>Model Container</th>
              <th>Tip Container</th>
              <th>Număr Colete</th>
              <th>Greutate Brută</th>
              <th>Descriere Marfă</th>
              <th>Tip Operațiune</th>
              <th>Nume Navă</th>
              <th>Pavilion Navă</th>
              <th>Număr Sumară</th>
              <th>Linie Maritimă</th>
            </tr>
          </thead>
          <tbody>
            {results.results.map((entry) => (
              <tr key={entry.id}>
                <td>{formatNumber(entry.numar_curent)}</td>
                <td>{entry.numar_manifest || '-'}</td>
                <td>{entry.numar_permis || '-'}</td>
                <td>{entry.numar_pozitie || '-'}</td>
                <td>{entry.cerere_operatiune || '-'}</td>
                <td>{formatDate(entry.data_inregistrare)}</td>
                <td className="highlight">{entry.container || '-'}</td>
                <td>{entry.model_container || '-'}</td>
                <td>{entry.tip_container || '-'}</td>
                <td>{formatNumber(entry.numar_colete)}</td>
                <td>{entry.greutate_bruta ? `${entry.greutate_bruta} kg` : '-'}</td>
                <td className="description">{entry.descriere_marfa || '-'}</td>
                <td>{entry.tip_operatiune || '-'}</td>
                <td>{entry.nume_nava || '-'}</td>
                <td>{entry.pavilion_nava || '-'}</td>
                <td>{entry.numar_sumara || '-'}</td>
                <td>{entry.linie_maritima || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {results.next && (
        <div className="pagination-info">
          <p>Afișate primele {results.results.length} rezultate din {results.count}</p>
        </div>
      )}
    </div>
  );
}

export default ResultsTable;
