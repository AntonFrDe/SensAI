import { useEffect, useState } from 'react';

export type Preferences = {
  theme: 'dark' | 'light';
  deck: 'two-colors' | 'four-colors';
  cardSize: 'normal' | 'large';
  motion: 'on' | 'off';
};

export const defaultPreferences: Preferences = { theme: 'dark', deck: 'two-colors', cardSize: 'normal', motion: 'on' };
const storageKey = 'sensai-preferences';
const allowed: { [Key in keyof Preferences]: Preferences[Key][] } = {
  theme: ['dark', 'light'], deck: ['two-colors', 'four-colors'], cardSize: ['normal', 'large'], motion: ['on', 'off'],
};

export function loadPreferences(storage: Storage = localStorage): Preferences {
  try {
    const saved = JSON.parse(storage.getItem(storageKey) ?? '{}');
    const result = { ...defaultPreferences };
    for (const key of Object.keys(allowed) as (keyof Preferences)[]) {
      if ((allowed[key] as string[]).includes(saved?.[key])) Object.assign(result, { [key]: saved[key] });
    }
    return result;
  } catch {
    return { ...defaultPreferences };
  }
}

export function applyPreferences(preferences: Preferences, root: HTMLElement = document.documentElement): void {
  root.dataset.theme = preferences.theme;
  root.dataset.deck = preferences.deck;
  root.dataset.cardSize = preferences.cardSize;
  root.dataset.motion = preferences.motion;
}

export function savePreferences(preferences: Preferences, storage: Storage = localStorage): boolean {
  try {
    storage.setItem(storageKey, JSON.stringify(preferences));
    return true;
  } catch {
    return false;
  }
}

export function usePreferences(): [Preferences, (change: Partial<Preferences>) => void] {
  const [preferences, setPreferences] = useState<Preferences>(() => loadPreferences());
  useEffect(() => {
    applyPreferences(preferences);
    savePreferences(preferences);
  }, [preferences]);
  return [preferences, change => setPreferences(previous => ({ ...previous, ...change }))];
}
