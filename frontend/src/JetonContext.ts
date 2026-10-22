import { createContext, useContext } from 'react';

export type Palette = 'pink' | 'mint' | 'sky' | 'yel' | 'lav';
export type JetonLook = { palette: 'pink' | 'mint'; crown: boolean; shades: boolean };
export type JetonValue = { look: JetonLook; pokeLine: string; onPoke: () => void };

export const JetonContext = createContext<JetonValue>({
  look: { palette: 'pink', crown: false, shades: false },
  pokeLine: '',
  onPoke: () => undefined,
});

export function useJeton(): JetonValue {
  return useContext(JetonContext);
}
