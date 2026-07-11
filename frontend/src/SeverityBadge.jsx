export default function SeverityBadge({ severity }) {
  return (
    <span className={`severity-badge severity-${severity.toLowerCase()}`}>
      {severity.toUpperCase()}
    </span>
  );
}
