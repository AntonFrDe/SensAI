import { createContext, useContext } from 'react';

export type Palette = 'pink' | 'mint' | 'sky' | 'yel' | 'lav';
export type JetonValue = { pokeLine: string; onPoke: () => void };

export const JetonContext = createContext<JetonValue>({
  pokeLine: '',
  onPoke: () => undefined,
});

export function useJeton(): JetonValue {
  return useContext(JetonContext);
}
