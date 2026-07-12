import { useState, useEffect } from 'react';
import SeverityBadge from './SeverityBadge';

const API_BASE = 'http://localhost:8000';

export default function ExceptionDetail({ exceptionId, onClose }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/exceptions/${exceptionId}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch exception details');
        return res.json();
      })
      .then(data => {
        setDetail(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [exceptionId]);

  return (
    <div className="detail-panel">
      <div className="detail-header">
        <h2>Exception Details</h2>
        <button className="close-btn" onClick={onClose}>✕</button>
      </div>

      {loading && <div className="detail-content">Loading...</div>}
      {error && <div className="detail-content error">{error}</div>}
      
      {!loading && !error && detail && (
        <div className="detail-content">
          <div className="detail-summary">
            <h3>{detail.product_code}</h3>
            <p><strong>Date:</strong> {detail.date}</p>
            <p><strong>Planned vs Actual:</strong> {detail.planned_units} / {detail.actual_units}</p>
            <p><strong>Deficit %:</strong> {(detail.deficit_pct * 100).toFixed(1)}%</p>
            <p>
              <strong>Severity:</strong> <SeverityBadge severity={detail.severity} />
            </p>
            <p>
              <strong>Status:</strong> <span className={`status-badge status-${detail.status}`}>{detail.status}</span>
            </p>
          </div>

          <div className="trend-section">
            <h4>7-Day Trend</h4>
            <table className="trend-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Planned</th>
                  <th>Actual</th>
                </tr>
              </thead>
              <tbody>
                {detail.last_7_days.map((day, idx) => (
                  <tr key={idx}>
                    <td>{day.date}</td>
                    <td>{day.planned_units}</td>
                    <td>{day.actual_units}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
