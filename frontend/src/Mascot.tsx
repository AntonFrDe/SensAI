import { useEffect, useRef, useState, type ReactElement } from 'react';
import { useJeton, type Palette } from './JetonContext';
import { mouvementReduit } from './motion';
import { SFX } from './sfx';

export type Mood = 'idle' | 'happy' | 'sad' | 'think' | 'wow' | 'sleep';

export type MascotProps = {
  mood: Mood;
  size: number;
  opponent?: Palette;
  pokable?: boolean;
};

const PALETTES: Record<Palette, [string, string, string]> = {
  pink: ['#FF4F8B', '#FF77A6', '#FFB8CF'],
  mint: ['#12C487', '#5FEBB5', '#C2F8E2'],
  sky: ['#1FA8F0', '#6CD2FF', '#C7EEFF'],
  yel: ['#F2A90F', '#FFD76B', '#FFF1C4'],
  lav: ['#8B66FF', '#B49CFF', '#E0D5FF'],
};

function bouche(mood: Mood): ReactElement {
  switch (mood) {
    case 'happy':
      return <><path d="M35 60 Q50 80 65 60 Z" fill="#4A0C26" /><path d="M42 68 Q50 75 58 68" fill="#FF8FB3" /></>;
    case 'sad':
      return <path d="M39 70 Q50 60 61 70" stroke="#4A0C26" strokeWidth={4.5} fill="none" strokeLinecap="round" />;
    case 'think':
      return <path d="M42 67 Q50 62 58 66" stroke="#4A0C26" strokeWidth={4.5} fill="none" strokeLinecap="round" />;
    case 'wow':
      return <ellipse cx="50" cy="67" rx="6.5" ry="8" fill="#4A0C26" />;
    case 'sleep':
      return <ellipse cx="50" cy="67" rx="3.5" ry="3" fill="#4A0C26" />;
    default:
      return <path d="M40 62 Q50 71 60 62" stroke="#4A0C26" strokeWidth={4.5} fill="none" strokeLinecap="round" />;
  }
}

export default function Mascot({ mood, size, opponent, pokable = !opponent }: MascotProps) {
  const { onPoke } = useJeton();
  const palette = opponent ?? 'pink';
  const couleurs = PALETTES[palette];
  const [retard] = useState(() => Math.random() * 3);
  const [flash, setFlash] = useState<{ mood: Mood; id: number } | null>(null);
  const svg = useRef<SVGSVGElement>(null);
  const pupilles = useRef<SVGGElement>(null);
  const affiche = flash?.mood ?? mood;
  const triste = affiche === 'sad';

  useEffect(() => {
    const suivre = (event: PointerEvent) => {
      const groupe = pupilles.current;
      const cadre = svg.current;
      if (!groupe || !cadre) return;
      const boite = cadre.getBoundingClientRect();
      const dx = event.clientX - (boite.left + boite.width / 2);
      const dy = event.clientY - (boite.top + boite.height * 0.44);
      const distance = Math.hypot(dx, dy) || 1;
      const k = Math.min(1, distance / 140) * 3.4;
      groupe.setAttribute('transform', `translate(${((dx / distance) * k).toFixed(2)} ${((dy / distance) * k).toFixed(2)})`);
    };
    const revenir = () => pupilles.current?.removeAttribute('transform');
    window.addEventListener('pointermove', suivre);
    document.documentElement.addEventListener('pointerleave', revenir);
    return () => {
      window.removeEventListener('pointermove', suivre);
      document.documentElement.removeEventListener('pointerleave', revenir);
    };
  }, []);

  useEffect(() => {
    if (!flash) return undefined;
    const minuterie = window.setTimeout(() => setFlash(null), 800);
    return () => window.clearTimeout(minuterie);
  }, [flash]);

  function poke() {
    SFX.poke();
    onPoke();
    setFlash(precedent => ({ mood: 'happy', id: (precedent?.id ?? 0) + 1 }));
    if (!mouvementReduit()) {
      svg.current?.animate?.([
        { transform: 'rotate(0) scale(1)' },
        { transform: 'rotate(-20deg) scale(1.2,.8)', offset: 0.25 },
        { transform: 'rotate(360deg) scale(1)' },
      ], { duration: 650, easing: 'cubic-bezier(.3,1.5,.5,1)' });
    }
  }

  const dessin = (
    <svg
      ref={svg}
      className={`jt-masc jt-mood-${affiche}`}
      width={size}
      height={size}
      viewBox="0 0 100 100"
      aria-hidden="true"
      style={{ animationDelay: `${-retard}s` }}
    >
      <ellipse cx="50" cy="98" rx="30" ry="4" fill="rgba(0,0,0,.25)" />
      <circle cx="50" cy="50" r="46" fill={couleurs[0]} />
      <circle cx="50" cy="50" r="42.5" fill="none" stroke="#fff" strokeWidth={7} strokeDasharray="11 11.2" />
      <circle cx="50" cy="50" r="32" fill={couleurs[1]} />
      {affiche === 'sleep' ? (
        <>
          <path d="M31 45 Q38.5 52 46 45" stroke="#2A0B1C" strokeWidth={4} fill="none" strokeLinecap="round" />
          <path d="M54 45 Q61.5 52 69 45" stroke="#2A0B1C" strokeWidth={4} fill="none" strokeLinecap="round" />
          <text className="jt-zz" x="76" y="20" fontSize={17} fontWeight={900} fill="#fff">z</text>
        </>
      ) : (
        <g className="jt-eyes">
          <ellipse cx="39" cy="44" rx="8.5" ry={triste ? 8 : 10} fill="#fff" />
          <ellipse cx="61" cy="44" rx="8.5" ry={triste ? 8 : 10} fill="#fff" />
          <g ref={pupilles} className="jt-pups">
            <circle cx="39" cy="45" r="5.2" fill="#2A0B1C" />
            <circle cx="61" cy="45" r="5.2" fill="#2A0B1C" />
            <circle cx="41" cy="42.5" r="1.9" fill="#fff" />
            <circle cx="63" cy="42.5" r="1.9" fill="#fff" />
          </g>
        </g>
      )}
      <ellipse cx="27" cy="57" rx="5.5" ry="3.2" fill={couleurs[2]} />
      <ellipse cx="73" cy="57" rx="5.5" ry="3.2" fill={couleurs[2]} />
      {triste && <path d="M30 31 L44 35 M70 31 L56 35" stroke="#4A0C26" strokeWidth={3.5} strokeLinecap="round" />}
      <g className="jt-bouche">{bouche(affiche)}</g>
    </svg>
  );

  if (!pokable) return dessin;
  return (
    <button type="button" className="jt-mbtn" onClick={poke} aria-label="Jeton, la mascotte">
      {dessin}
    </button>
  );
}
