export type CarteTableProps = { code: string; animation: 'deal' | 'flip'; delai: number };

const SYMBOLES: Record<string, string> = { s: '♠', h: '♥', d: '♦', c: '♣' };

export default function CarteTable({ code, animation, delai }: CarteTableProps) {
  const rang = code[0] === 'T' ? '10' : code[0];
  const symbole = SYMBOLES[code[1]] ?? code[1];
  const rouge = symbole === '♥' || symbole === '♦';
  const face = (
    <span className="jt-face">
      <b>{rang}</b>
      <span>{symbole}</span>
    </span>
  );
  if (animation === 'deal') {
    return (
      <span className={`jt-c3 jt-deal${rouge ? ' jt-red' : ''}`} style={{ animationDelay: `${delai}ms` }}>
        <span className="jt-in" style={{ animation: 'none' }}>{face}</span>
      </span>
    );
  }
  return (
    <span className={`jt-c3 jt-tilt${rouge ? ' jt-red' : ''}`}>
      <span className="jt-in" style={{ animationDelay: `${delai}ms` }}>
        {face}
        <span className="jt-back-face" />
      </span>
    </span>
  );
}
