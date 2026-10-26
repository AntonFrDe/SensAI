type Note = [frequence: number, debut: number, duree: number, frequenceFin?: number];

let actif = true;
let contexte: AudioContext | null = null;

export function sonActif(valeur: boolean): void {
  actif = valeur;
}

function jouer(notes: Note[], type: OscillatorType = 'triangle', volume = 0.09): void {
  if (!actif) return;
  try {
    const Contexte = window.AudioContext ?? (window as Window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Contexte) return;
    const ctx = contexte ?? new Contexte();
    contexte = ctx;
    const t0 = ctx.currentTime + 0.01;
    for (const [frequence, debut, duree, frequenceFin] of notes) {
      const oscillateur = ctx.createOscillator();
      const gain = ctx.createGain();
      oscillateur.type = type;
      oscillateur.frequency.setValueAtTime(frequence, t0 + debut);
      if (frequenceFin) oscillateur.frequency.exponentialRampToValueAtTime(frequenceFin, t0 + debut + duree);
      gain.gain.setValueAtTime(0.0001, t0 + debut);
      gain.gain.exponentialRampToValueAtTime(volume, t0 + debut + 0.012);
      gain.gain.exponentialRampToValueAtTime(0.0001, t0 + debut + duree);
      oscillateur.connect(gain).connect(ctx.destination);
      oscillateur.start(t0 + debut);
      oscillateur.stop(t0 + debut + duree + 0.03);
    }
  } catch {
  }
}

export const SFX = {
  pop: () => jouer([[520, 0, 0.08, 820]], 'sine', 0.06),
  bon: () => jouer([[523, 0, 0.12], [659, 0.09, 0.12], [784, 0.18, 0.12], [1047, 0.27, 0.3]]),
  mauvais: () => jouer([[392, 0, 0.2, 330], [311, 0.18, 0.35, 233]], 'sine', 0.08),
  xp: () => jouer([[988, 0, 0.07], [1319, 0.06, 0.14]], 'square', 0.025),
  niveau: () => jouer([[523, 0, 0.14], [659, 0.12, 0.14], [784, 0.24, 0.14], [1047, 0.36, 0.22], [784, 0.58, 0.1], [1047, 0.68, 0.5]], 'triangle', 0.1),
  poke: () => jouer([[280, 0, 0.16, 760]], 'sine', 0.08),
  carte: () => jouer([[1500, 0, 0.035, 900]], 'square', 0.015),
  tic: () => jouer([[180, 0, 0.06, 120]], 'square', 0.03),
};
