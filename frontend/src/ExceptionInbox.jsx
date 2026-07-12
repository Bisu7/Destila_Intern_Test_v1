import { useState, useEffect } from 'react';
import DayGroup from './DayGroup';
import ExceptionDetail from './ExceptionDetail';

const API_BASE = 'http://localhost:8000';

export default function ExceptionInbox() {
  const [exceptions, setExceptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedExceptionId, setSelectedExceptionId] = useState(null);
  
  const [filterProduct, setFilterProduct] = useState('');
  const [filterSeverity, setFilterSeverity] = useState('');
  const [allProducts, setAllProducts] = useState([]);

  // Fetch unique products once on mount to populate the dropdown fully
  useEffect(() => {
    fetch(`${API_BASE}/exceptions`)
      .then(res => res.json())
      .then(data => {
        const products = [...new Set(data.map(e => e.product_code))];
        setAllProducts(products.sort());
      });
  }, []);

  // Fetch exceptions whenever filters change
  useEffect(() => {
    setLoading(true);
    let url = new URL(`${API_BASE}/exceptions`);
    if (filterProduct) url.searchParams.append('product_code', filterProduct);
    if (filterSeverity) url.searchParams.append('severity', filterSeverity);

    fetch(url)
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
  }, [filterProduct, filterSeverity]);

  const handleStatusUpdate = (updatedExc) => {
    setExceptions(prev => prev.map(exc => 
      exc.id === updatedExc.id ? { ...exc, status: updatedExc.status } : exc
    ));
  };

  const grouped = exceptions.reduce((acc, exc) => {
    if (!acc[exc.date]) acc[exc.date] = [];
    acc[exc.date].push(exc);
    return acc;
  }, {});

  const orderedDates = [...new Set(exceptions.map(e => e.date))];

  return (
    <div className="inbox-container">
      <div className="filters">
        <select 
          value={filterProduct} 
          onChange={(e) => setFilterProduct(e.target.value)}
          className="filter-select"
        >
          <option value="">All Products</option>
          {allProducts.map(p => (
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
        
        <select 
          value={filterSeverity} 
          onChange={(e) => setFilterSeverity(e.target.value)}
          className="filter-select"
        >
          <option value="">All Severities</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
        </select>
      </div>

      {loading && <div>Loading exceptions...</div>}
      {error && <div className="error">Error: {error}</div>}

      {!loading && !error && (
        <div className="inbox-layout">
          <div className="inbox-main">
            {orderedDates.length === 0 ? (
              <div className="empty-state">No exceptions match your filters.</div>
            ) : (
              orderedDates.map(date => (
                <DayGroup 
                  key={date} 
                  date={date} 
                  exceptions={grouped[date]} 
                  selectedExceptionId={selectedExceptionId}
                  onSelectException={setSelectedExceptionId}
                />
              ))
            )}
          </div>

          {selectedExceptionId && (
            <div className="inbox-side">
              <ExceptionDetail 
                exceptionId={selectedExceptionId} 
                onClose={() => setSelectedExceptionId(null)}
                onStatusUpdate={handleStatusUpdate}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
