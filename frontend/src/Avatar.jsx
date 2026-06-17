const PALETTE = [
  { bg: '#E3EBDB', fg: '#587349' },
  { bg: '#FBE9DD', fg: '#9C5B36' },
  { bg: '#FBEAE6', fg: '#9C3B2E' },
  { bg: '#DCE8D5', fg: '#3F5A37' },
];

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

function getInitials(name) {
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

export default function Avatar({ name, size = 40 }) {
  const colors = PALETTE[hashString(name) % PALETTE.length];
  return (
    <div
      className="avatar"
      style={{
        width: size,
        height: size,
        background: colors.bg,
        color: colors.fg,
        fontSize: size * 0.38,
      }}
    >
      {getInitials(name)}
    </div>
  );
}