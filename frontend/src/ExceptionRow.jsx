import SeverityBadge from './SeverityBadge';

export default function ExceptionRow({ exception, isSelected, onSelect }) {
  const deficitPctFormat = (exception.deficit_pct * 100).toFixed(1) + '%';
  
  return (
    <div 
      className={`exception-row row-layout ${isSelected ? 'selected' : ''}`}
      onClick={onSelect}
    >
      <div className="col font-bold">{exception.product_code}</div>
      <div className="col">
        {exception.planned_units} / {exception.actual_units}
      </div>
      <div className="col text-red">{deficitPctFormat}</div>
      <div className="col">
        <SeverityBadge severity={exception.severity} />
      </div>
      <div className="col status-cell">
        <span className={`status-badge status-${exception.status}`}>
          {exception.status}
        </span>
      </div>
    </div>
  );
}
