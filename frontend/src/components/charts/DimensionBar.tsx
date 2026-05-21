interface DimensionBarProps {
  label: string;
  score: number;
  maxScore?: number;
}

export function DimensionBar({ label, score, maxScore = 20 }: DimensionBarProps) {
  const percentage = (score / maxScore) * 100;

  // Color based on score relative to 20
  let colorClass = "bg-red-500";
  if (score >= 15) colorClass = "bg-green-500";
  else if (score >= 10) colorClass = "bg-yellow-500";

  return (
    <div className="mb-4">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-slate-700">{label}</span>
        <span className="text-sm font-medium text-slate-700">{score}/{maxScore}</span>
      </div>
      <div className="w-full bg-slate-200 rounded-full h-2.5">
        <div className={`h-2.5 rounded-full ${colorClass}`} style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  );
}
