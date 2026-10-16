import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import HandInfo from './HandInfo';

describe('HandInfo', () => {
  it('translates the phase and shows the current bet', () => {
    render(<HandInfo phase="showdown" currentBet={40} />);
    expect(screen.getByText(/Phase/)).toHaveTextContent('Phase : Abattage');
    expect(screen.getByText(/Mise actuelle/)).toHaveTextContent('Mise actuelle : 40 jetons');
  });

  it('shows dashes before the first hand', () => {
    render(<HandInfo />);
    expect(screen.getByText(/Phase/)).toHaveTextContent('Phase : —');
  });
});
