import type { Preferences } from './preferences';

export type PreferencesPanelProps = { preferences: Preferences; onChange: (change: Partial<Preferences>) => void };

type Choice<Key extends keyof Preferences> = { key: Key; legend: string; options: { value: Preferences[Key]; label: string }[] };

const choices = [
  { key: 'theme', legend: 'Thème', options: [{ value: 'dark', label: 'Sombre' }, { value: 'light', label: 'Clair' }] },
  { key: 'deck', legend: 'Couleurs des cartes', options: [
    { value: 'two-colors', label: 'Deux couleurs' }, { value: 'four-colors', label: 'Quatre couleurs (♦ bleu, ♣ vert)' },
  ] },
  { key: 'cardSize', legend: 'Taille des cartes', options: [{ value: 'normal', label: 'Normale' }, { value: 'large', label: 'Grande' }] },
  { key: 'motion', legend: 'Animations', options: [{ value: 'on', label: 'Activées' }, { value: 'off', label: 'Désactivées' }] },
] as Choice<keyof Preferences>[];

export default function PreferencesPanel({ preferences, onChange }: PreferencesPanelProps) {
  return (
    <details className="preferences">
      <summary>Préférences d’affichage</summary>
      <div className="preferences-grid">
        {choices.map(choice => (
          <fieldset key={choice.key}>
            <legend>{choice.legend}</legend>
            {choice.options.map(option => (
              <label key={option.value} className="choice">
                <input type="radio" name={`preference-${choice.key}`} value={option.value}
                  checked={preferences[choice.key] === option.value}
                  onChange={() => onChange({ [choice.key]: option.value })} />
                {option.label}
              </label>
            ))}
          </fieldset>
        ))}
      </div>
    </details>
  );
}
