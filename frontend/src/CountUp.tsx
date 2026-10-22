import { useEffect, useRef, useState } from 'react';
import { mouvementReduit } from './motion';

export type CountUpProps = { valeur: number; suffixe?: string; duree?: number };

export default function CountUp({ valeur, suffixe = '', duree = 700 }: CountUpProps) {
  const [affiche, setAffiche] = useState(valeur);
  const depart = useRef(valeur);

  useEffect(() => {
    const a = depart.current;
    depart.current = valeur;
    if (mouvementReduit() || typeof requestAnimationFrame !== 'function') {
      setAffiche(valeur);
      return undefined;
    }
    const debut = performance.now();
    let image = 0;
    const etape = (instant: number) => {
      const progression = Math.min(1, (instant - debut) / duree);
      setAffiche(Math.round(a + (valeur - a) * (1 - Math.pow(1 - progression, 3))));
      if (progression < 1) image = requestAnimationFrame(etape);
    };
    image = requestAnimationFrame(etape);
    return () => cancelAnimationFrame(image);
  }, [valeur, duree]);

  return <>{affiche}{suffixe}</>;
}
