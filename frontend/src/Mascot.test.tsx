import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import Mascot from './Mascot';

describe('Mascot', () => {
  it('shows the mood as a class of the drawing', () => {
    const { container } = render(<Mascot mood="happy" size={48} />);
    expect(container.querySelector('svg.jt-masc')).toHaveClass('jt-mood-happy');
  });

  it('draws a sleeping Jeton with closed eyes and a z', () => {
    const { container } = render(<Mascot mood="sleep" size={48} />);
    expect(container.querySelector('.jt-zz')).toHaveTextContent('z');
    expect(container.querySelector('.jt-pups')).toBeNull();
  });

  it('draws the opponent in its own colour', () => {
    const { container } = render(<Mascot mood="sleep" size={48} opponent="sky" />);
    expect(container.querySelector('circle')).toHaveAttribute('fill', '#1FA8F0');
  });

  it('always draws the main Jeton pink, without accessories nor button', () => {
    const { container } = render(<Mascot mood="idle" size={90} />);
    expect(screen.queryByRole('button')).toBeNull();
    expect(container.querySelector('circle')).toHaveAttribute('fill', '#FF4F8B');
    expect(container.querySelectorAll('rect')).toHaveLength(0);
  });
});
