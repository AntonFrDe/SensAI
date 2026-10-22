import { useState, type CSSProperties } from 'react';
import { mouvementReduit } from './motion';

const COULEURS = ['#FF4F8B', '#FFC83D', '#3EC5FF', '#2EE59D', '#A98BFF'];

export type ParticulesProps = { nombre: number; distance: number; duree: number; grand?: boolean };

type Particule = { x: number; y: number; r: number; taille: number; hauteur: number; arrondie: boolean; dur: number; couleur: string };

function generer(nombre: number, distance: number, duree: number, grand: boolean): Particule[] {
  return Array.from({ length: nombre }, (_, i) => {
    const taille = (grand ? 7 : 4) + Math.random() * (grand ? 9 : 4);
    const angle = grand ? Math.random() * Math.PI * 2 : (i / nombre) * Math.PI * 2;
    const vitesse = distance * (0.5 + Math.random() * 0.7);
    return {
      x: Math.cos(angle) * vitesse,
      y: Math.sin(angle) * vitesse * (grand ? 0.7 : 1) + (grand ? 200 : 0),
      r: Math.random() * 900,
      taille,
      hauteur: grand && Math.random() < 0.5 ? taille * 0.5 : taille,
      arrondie: Math.random() < 0.6,
      dur: duree * (0.8 + Math.random() * 0.5),
      couleur: COULEURS[i % 5],
    };
  });
}

export default function Particules({ nombre, distance, duree, grand = false }: ParticulesProps) {
  const [particules] = useState(() => (mouvementReduit() ? [] : generer(nombre, distance, duree, grand)));
  return (
    <span className="jt-burst" aria-hidden="true">
      {particules.map((particule, index) => (
        <i
          key={index}
          className="jt-part"
          style={{
            width: particule.taille,
            height: particule.hauteur,
            borderRadius: particule.arrondie ? '50%' : '3px',
            background: particule.couleur,
            zIndex: 38,
            '--x': `${particule.x}px`,
            '--y': `${particule.y}px`,
            '--r': `${particule.r}deg`,
            '--dur': `${particule.dur}ms`,
          } as CSSProperties}
        />
      ))}
    </span>
  );
}
