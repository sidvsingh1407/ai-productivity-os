import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

interface ScoreRadarChartProps {
  data: {
    subject: string;
    A: number;
    fullMark: number;
  }[];
}

export function ScoreRadarChart({ data }: ScoreRadarChartProps) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="subject" />
        <PolarRadiusAxis angle={30} domain={[0, 20]} />
        <Radar name="Score" dataKey="A" stroke="#0f172a" fill="#334155" fillOpacity={0.6} />
        <Tooltip />
      </RadarChart>
    </ResponsiveContainer>
  );
}
