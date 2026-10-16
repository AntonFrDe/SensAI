import { describe, expect, it } from 'vitest';
import { isTypingTarget, shortcutAction } from './shortcuts';

describe('shortcutAction', () => {
  it('maps F and C to the legal simple actions', () => {
    expect(shortcutAction('f', ['fold', 'call'], false)).toEqual({ type: 'play', action: 'fold' });
    expect(shortcutAction('C', ['fold', 'call'], false)).toEqual({ type: 'play', action: 'call' });
    expect(shortcutAction('c', ['fold', 'check', 'bet'], false)).toEqual({ type: 'play', action: 'check' });
  });

  it('plays a bet or raise only with a valid amount', () => {
    expect(shortcutAction('r', ['fold', 'call', 'raise'], true)).toEqual({ type: 'play', action: 'raise' });
    expect(shortcutAction('b', ['fold', 'check', 'bet'], true)).toEqual({ type: 'play', action: 'bet' });
    expect(shortcutAction('r', ['fold', 'call', 'raise'], false)).toEqual({ type: 'focus-amount' });
    expect(shortcutAction('t', ['fold', 'check', 'bet'], false)).toEqual({ type: 'all-in' });
  });

  it('ignores illegal actions and other keys', () => {
    expect(shortcutAction('r', ['fold', 'call'], true)).toBeNull();
    expect(shortcutAction('t', ['fold', 'call'], true)).toBeNull();
    expect(shortcutAction('f', [], true)).toBeNull();
    expect(shortcutAction('x', ['fold', 'call'], true)).toBeNull();
  });
});

describe('isTypingTarget', () => {
  it('recognises fields where letters are text', () => {
    expect(isTypingTarget(document.createElement('input'))).toBe(true);
    expect(isTypingTarget(document.createElement('textarea'))).toBe(true);
    expect(isTypingTarget(document.createElement('button'))).toBe(false);
    expect(isTypingTarget(null)).toBe(false);
  });
});
