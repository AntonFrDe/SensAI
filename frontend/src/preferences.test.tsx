import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import PreferencesPanel from './PreferencesPanel';
import PlayingCard from './PlayingCard';
import { applyPreferences, defaultPreferences, loadPreferences, savePreferences } from './preferences';

describe('preferences', () => {
  beforeEach(() => localStorage.clear());

  it('keeps only known values when loading', () => {
    savePreferences({ ...defaultPreferences, theme: 'light', deck: 'four-colors' });
    expect(loadPreferences()).toEqual({ ...defaultPreferences, theme: 'light', deck: 'four-colors' });
    localStorage.setItem('sensai-preferences', JSON.stringify({ theme: 'neon', cardSize: 'large' }));
    expect(loadPreferences()).toEqual({ ...defaultPreferences, cardSize: 'large' });
    localStorage.setItem('sensai-preferences', '{broken');
    expect(loadPreferences()).toEqual(defaultPreferences);
  });

  it('applies them as data attributes on the page', () => {
    const root = document.createElement('html');
    applyPreferences({ theme: 'light', deck: 'four-colors', cardSize: 'large', motion: 'off' }, root);
    expect(root.dataset).toMatchObject({ theme: 'light', deck: 'four-colors', cardSize: 'large', motion: 'off' });
  });

  it('marks each card with its suit for the four-colour deck', () => {
    render(<PlayingCard card={{ rank: '5', suit: 'clubs' }} />);
    expect(screen.getByRole('img', { name: '5 de trèfle' })).toHaveClass('suit-clubs');
  });
});

describe('PreferencesPanel', () => {
  it('reports each change', async () => {
    const onChange = vi.fn();
    render(<PreferencesPanel preferences={defaultPreferences} onChange={onChange} />);
    await userEvent.click(screen.getByText('Préférences d’affichage'));
    expect(screen.getByRole('radio', { name: 'Sombre' })).toBeChecked();
    await userEvent.click(screen.getByRole('radio', { name: 'Clair' }));
    await userEvent.click(screen.getByRole('radio', { name: /Quatre couleurs/ }));
    await userEvent.click(screen.getByRole('radio', { name: 'Désactivées' }));
    expect(onChange.mock.calls.map(call => call[0])).toEqual([{ theme: 'light' }, { deck: 'four-colors' }, { motion: 'off' }]);
  });
});
