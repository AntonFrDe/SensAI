import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import Mascot from './Mascot';
import { JetonContext, type JetonLook } from './JetonContext';

function renderIn(ui: React.ReactElement, look: JetonLook = { palette: 'pink', crown: false, shades: false }, onPoke = vi.fn()) {
  render(<JetonContext.Provider value={{ look, pokeLine: '', onPoke }}>{ui}</JetonContext.Provider>);
  return onPoke;
}

describe('Mascot', () => {
  it('shows the mood as a class of the drawing', () => {
    const { container } = render(<JetonContext.Provider value={{ look: { palette: 'pink', crown: false, shades: false }, pokeLine: '', onPoke: vi.fn() }}><Mascot mood="happy" size={48} /></JetonContext.Provider>);
    expect(container.querySelector('svg.jt-masc')).toHaveClass('jt-mood-happy');
  });

  it('draws a sleeping Jeton with closed eyes and a z', () => {
    const { container } = render(<JetonContext.Provider value={{ look: { palette: 'pink', crown: false, shades: false }, pokeLine: '', onPoke: vi.fn() }}><Mascot mood="sleep" size={48} /></JetonContext.Provider>);
    expect(container.querySelector('.jt-zz')).toHaveTextContent('z');
    expect(container.querySelector('.jt-pups')).toBeNull();
  });

  it('pokes the main Jeton through a labelled button', async () => {
    const onPoke = renderIn(<Mascot mood="idle" size={90} />);
    await userEvent.click(screen.getByRole('button', { name: 'Jeton, la mascotte' }));
    expect(onPoke).toHaveBeenCalledOnce();
  });

  it('draws the opponent in its own colour without a button or accessories', () => {
    const { container } = render(<JetonContext.Provider value={{ look: { palette: 'pink', crown: true, shades: true }, pokeLine: '', onPoke: vi.fn() }}><Mascot mood="sleep" size={48} opponent="sky" /></JetonContext.Provider>);
    expect(screen.queryByRole('button')).toBeNull();
    expect(container.querySelector('circle')).toHaveAttribute('fill', '#1FA8F0');
    expect(container.querySelectorAll('rect')).toHaveLength(0);
    expect(container.querySelectorAll('path[stroke="#FFC83D"], path[fill="#FFC83D"]')).toHaveLength(0);
  });

  it('wears the crown and the shades earned by the player', () => {
    const { container } = render(<JetonContext.Provider value={{ look: { palette: 'mint', crown: true, shades: true }, pokeLine: '', onPoke: vi.fn() }}><Mascot mood="idle" size={90} /></JetonContext.Provider>);
    expect(container.querySelectorAll('rect')).toHaveLength(2);
    expect(container.querySelector('path[fill="#FFC83D"]')).not.toBeNull();
    expect(container.querySelector('circle[fill="#12C487"]')).not.toBeNull();
  });
});
