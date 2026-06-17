// Single source of truth for turning a numeric match_score into a tier.
// Both ChartPanel and ResultsPanel import this so the pie chart and the
// candidate list can never disagree about what counts as a strong/
// moderate/weak match.

export function matchTier(score) {
  if (typeof score !== 'number') return null;
  if (score >= 80) return 'Strong match';
  if (score >= 50) return 'Moderate match';
  return 'Weak match';
}

export function tierPillClass(tier) {
  if (tier === 'Strong match') return 'pill-strong';
  if (tier === 'Moderate match') return 'pill-moderate';
  return 'pill-weak';
}
