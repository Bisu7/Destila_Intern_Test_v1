import { useState } from 'react';
import ExceptionRow from './ExceptionRow';

export default function DayGroup({ date, exceptions, selectedExceptionId, onSelectException }) {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="day-group">
      <div 
        className="day-header" 
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <h3>{date}</h3>
        <span className="badge-count">{exceptions.length} exception(s)</span>
        <span className="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
      </div>
      
      {isExpanded && (
        <div className="day-content">
          <div className="table-header row-layout">
            <div className="col">Product</div>
            <div className="col">Plan vs Actual</div>
            <div className="col">Deficit %</div>
            <div className="col">Severity</div>
            <div className="col">Status</div>
          </div>
          {exceptions.map(exc => (
            <ExceptionRow 
              key={exc.id} 
              exception={exc} 
              isSelected={exc.id === selectedExceptionId}
              onSelect={() => onSelectException(exc.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
