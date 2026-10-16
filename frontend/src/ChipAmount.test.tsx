import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import ChipAmount from './ChipAmount';

describe('ChipAmount', () => {
  it('formats amounts with French thousands separators', () => {
    render(<ChipAmount amount={12500} />);
    expect(screen.getByText(/jetons/)).toHaveTextContent(/^12\s500 jetons$/);
  });

  it('shows a dash when the amount is unknown', () => {
    render(<ChipAmount />);
    expect(screen.getByText('—')).toBeInTheDocument();
  });
});
