import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { matchTier } from './scoring';

const COLORS = {
  'Strong match': '#6B8F58',
  'Moderate match': '#CB8B49',
  'Weak match': '#9A9A8C',
  'Unclassified': '#C7C7BC',
};

export default function ChartPanel({ submissions }) {
  const completed = submissions.filter((s) => s.status === 'completed' && s.result);

  const counts = {};
  completed.forEach((sub) => {
    const category = matchTier(sub.result.match_score) || 'Unclassified';
    counts[category] = (counts[category] || 0) + 1;
  });

  const data = Object.entries(counts).map(([name, value]) => ({ name, value }));

  return (
    <div className="panel">
      <h3>Match breakdown</h3>
      {data.length === 0 ? (
        <p className="empty-state">Results will appear here as resumes are screened.</p>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={70}
            label={({ name, value }) => `${value}`}
          >
              {data.map((entry) => (
                <Cell key={entry.name} fill={COLORS[entry.name] || '#999'} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
