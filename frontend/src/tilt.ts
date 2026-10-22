import { mouvementReduit } from './motion';

export function ecouterInclinaisons(racine: HTMLElement): () => void {
  let dernier: HTMLElement | null = null;
  const reinitialiser = () => {
    if (dernier) dernier.style.transform = '';
    dernier = null;
  };
  const deplacer = (event: PointerEvent) => {
    const cible = event.target instanceof Element ? event.target.closest<HTMLElement>('.jt-tilt') : null;
    if (dernier !== cible) reinitialiser();
    if (!cible || mouvementReduit()) return;
    const boite = cible.getBoundingClientRect();
    const x = (event.clientX - boite.left) / boite.width - 0.5;
    const y = (event.clientY - boite.top) / boite.height - 0.5;
    cible.style.transform = `perspective(600px) rotateX(${-y * 16}deg) rotateY(${x * 18}deg) translateY(-4px)`;
    cible.style.setProperty('--hx', `${(x + 0.5) * 100}%`);
    cible.style.setProperty('--hy', `${(y + 0.5) * 100}%`);
    dernier = cible;
  };
  racine.addEventListener('pointermove', deplacer);
  racine.addEventListener('pointerleave', reinitialiser);
  return () => {
    racine.removeEventListener('pointermove', deplacer);
    racine.removeEventListener('pointerleave', reinitialiser);
    reinitialiser();
  };
}
