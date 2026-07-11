import { useState, useEffect } from 'react';
import DayGroup from './DayGroup';

const API_BASE = 'http://localhost:8000';

export default function ExceptionInbox() {
  const [exceptions, setExceptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedExceptionId, setSelectedExceptionId] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/exceptions`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch exceptions');
        return res.json();
      })
      .then(data => {
        setExceptions(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading exceptions...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  const grouped = exceptions.reduce((acc, exc) => {
    if (!acc[exc.date]) acc[exc.date] = [];
    acc[exc.date].push(exc);
    return acc;
  }, {});

  const orderedDates = [...new Set(exceptions.map(e => e.date))];

  return (
    <div className="inbox">
      {orderedDates.map(date => (
        <DayGroup 
          key={date} 
          date={date} 
          exceptions={grouped[date]} 
          selectedExceptionId={selectedExceptionId}
          onSelectException={setSelectedExceptionId}
        />
      ))}
    </div>
  );
}
