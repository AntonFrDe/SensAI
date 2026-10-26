import { beforeEach, describe, expect, it } from 'vitest';
import {
  BADGES, PROGRESSION_INITIALE, avancementDuNiveau, chargerProgression, chatouiller,
  enregistrerProgression, jourDe, niveauDe, noterExercice, objectifDuJour, serieEnCours, type Progress,
} from './progress';

const lundi = '2026-10-19';
const mardi = '2026-10-20';
const mercredi = '2026-10-21';

function noter(progression: Progress, verdict: 'bon' | 'acceptable' | 'erreur', theme = 'ouverture', position = 'MP', jour = lundi) {
  return noterExercice(progression, { verdict, theme, position }, jour);
}

describe('noterExercice', () => {
  it('gives 20 XP for a good move, 10 for an acceptable one and 5 for a mistake', () => {
    expect(noter(PROGRESSION_INITIALE, 'bon').xp).toBe(20);
    expect(noter(PROGRESSION_INITIALE, 'acceptable').xp).toBe(10);
    expect(noter(PROGRESSION_INITIALE, 'erreur').xp).toBe(5);
  });

  it('adds the XP to the progression and counts the exercise', () => {
    const { progression } = noter({ ...PROGRESSION_INITIALE, xp: 100 }, 'bon');
    expect(progression.xp).toBe(120);
    expect(progression.exercices).toBe(1);
    expect(progression.bons).toBe(1);
  });

  it('builds a combo on good moves and breaks it on any other verdict', () => {
    const premier = noter(PROGRESSION_INITIALE, 'bon').progression;
    const deux = noter(premier, 'bon').progression;
    expect(deux.combo).toBe(2);
    expect(noter(deux, 'acceptable').progression.combo).toBe(0);
  });

  it('reports a level up only when the XP crosses a multiple of 500', () => {
    expect(noter({ ...PROGRESSION_INITIALE, xp: 490 }, 'bon').nouveauNiveau).toBe(true);
    expect(noter({ ...PROGRESSION_INITIALE, xp: 470 }, 'erreur').nouveauNiveau).toBe(false);
  });

  it('counts the daily goal of five exercises and resets it on a new day', () => {
    let progression = PROGRESSION_INITIALE;
    for (let i = 0; i < 3; i++) progression = noter(progression, 'erreur', 'ouverture', 'MP', lundi).progression;
    expect(objectifDuJour(progression, lundi)).toBe(3);
    expect(objectifDuJour(progression, mardi)).toBe(0);
    progression = noter(progression, 'erreur', 'ouverture', 'MP', mardi).progression;
    expect(objectifDuJour(progression, mardi)).toBe(1);
  });

  it('keeps the streak on the same day and extends it the day after', () => {
    const lundiFait = noter(PROGRESSION_INITIALE, 'bon', 'ouverture', 'MP', lundi).progression;
    expect(noter(lundiFait, 'bon', 'ouverture', 'MP', lundi).progression.serie).toBe(1);
    expect(noter(lundiFait, 'bon', 'ouverture', 'MP', mardi).progression.serie).toBe(2);
  });

  it('restarts the streak after a missed day', () => {
    const serie = { ...PROGRESSION_INITIALE, serie: 4, dernierJour: lundi };
    expect(noter(serie, 'bon', 'ouverture', 'MP', mercredi).progression.serie).toBe(1);
  });

  it('gives the king of the button badge for a good opening from the button, once', () => {
    const premier = noter(PROGRESSION_INITIALE, 'bon', 'ouverture', 'BTN');
    expect(premier.badges).toEqual([BADGES.roiDuBouton]);
    expect(premier.progression.badges).toEqual([BADGES.roiDuBouton]);
    expect(noter(premier.progression, 'bon', 'ouverture', 'BTN').badges).toEqual([]);
  });

  it('does not give the button badge for a good opening from another seat', () => {
    expect(noter(PROGRESSION_INITIALE, 'bon', 'ouverture', 'MP').badges).toEqual([]);
  });

  it('gives the draw hunter badge for a good draw decision', () => {
    expect(noter(PROGRESSION_INITIALE, 'bon', 'tirage', 'BB').badges).toEqual([BADGES.chasseurDeTirages]);
    expect(noter(PROGRESSION_INITIALE, 'erreur', 'tirage', 'BB').badges).toEqual([]);
  });

  it('gives the streak badge at seven days in a row', () => {
    const six = { ...PROGRESSION_INITIALE, serie: 6, dernierJour: lundi };
    expect(noter(six, 'erreur', 'ouverture', 'MP', mardi).badges).toEqual([BADGES.serie]);
  });
});

describe('chatouiller', () => {
  it('unlocks the secret badge at the sixth tickle only', () => {
    let progression = PROGRESSION_INITIALE;
    for (let i = 0; i < 5; i++) {
      const resultat = chatouiller(progression);
      expect(resultat.badges).toEqual([]);
      progression = resultat.progression;
    }
    const sixieme = chatouiller(progression);
    expect(sixieme.badges).toEqual([BADGES.chatouilleur]);
    expect(chatouiller(sixieme.progression).badges).toEqual([]);
  });
});

describe('niveaux', () => {
  it('derives the level and the bar from the XP', () => {
    expect(niveauDe(0)).toBe(1);
    expect(niveauDe(499)).toBe(1);
    expect(niveauDe(500)).toBe(2);
    expect(avancementDuNiveau(470)).toBeCloseTo(0.94);
  });
});

describe('serieEnCours', () => {
  it('is zero when the last exercise is older than yesterday', () => {
    const progression = { ...PROGRESSION_INITIALE, serie: 3, dernierJour: lundi };
    expect(serieEnCours(progression, mardi)).toBe(3);
    expect(serieEnCours(progression, mercredi)).toBe(0);
  });
});

describe('stockage local', () => {
  beforeEach(() => localStorage.clear());

  it('starts from the initial progression when nothing is stored', () => {
    expect(chargerProgression()).toEqual(PROGRESSION_INITIALE);
  });

  it('keeps what was saved', () => {
    enregistrerProgression({ ...PROGRESSION_INITIALE, xp: 240, badges: [BADGES.roiDuBouton] });
    expect(chargerProgression()).toMatchObject({ xp: 240, badges: [BADGES.roiDuBouton] });
  });

  it('ignores a corrupted entry', () => {
    localStorage.setItem('sensai-trainer-progress', '{pas du json');
    expect(chargerProgression()).toEqual(PROGRESSION_INITIALE);
  });

  it('formats the day in local time', () => {
    expect(jourDe(new Date(2026, 9, 5, 23, 59))).toBe('2026-10-05');
  });
});
