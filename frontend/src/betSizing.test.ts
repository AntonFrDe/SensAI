import { describe, expect, it } from 'vitest';
import { betPresets, clampAmount, potSizedTarget } from './betSizing';

describe('betSizing', () => {
  it('sizes an opening bet as a share of the pot', () => {
    expect(potSizedTarget(0.5, { pot: 80, toCall: 0, currentBet: 0 })).toBe(40);
    expect(potSizedTarget(1, { pot: 80, toCall: 0, currentBet: 0 })).toBe(80);
  });

  it('sizes a pot raise as call first, then raise the new pot', () => {
    expect(potSizedTarget(1, { pot: 30, toCall: 10, currentBet: 20 })).toBe(60);
  });

  it('keeps amounts inside the bounds of the server', () => {
    expect(clampAmount(12.4, 20, 100)).toBe(20);
    expect(clampAmount(57.6, 20, 100)).toBe(58);
    expect(clampAmount(500, 20, 100)).toBe(100);
  });

  it('offers min, pot shares and all-in without duplicates', () => {
    expect(betPresets({ pot: 100, toCall: 0, currentBet: 0, minAmount: 20, maxAmount: 900 })).toEqual([
      { label: 'Min', amount: 20 }, { label: '½ pot', amount: 50 }, { label: '¾ pot', amount: 75 },
      { label: 'Pot', amount: 100 }, { label: 'Tapis', amount: 900 },
    ]);
  });

  it('drops the shares that fall outside the bounds', () => {
    expect(betPresets({ pot: 30, toCall: 10, currentBet: 20, minAmount: 40, maxAmount: 50 })).toEqual([
      { label: 'Min', amount: 40 }, { label: 'Tapis', amount: 50 },
    ]);
  });

  it('gives a single all-in when the minimum is the whole stack', () => {
    expect(betPresets({ pot: 30, toCall: 10, currentBet: 20, minAmount: 60, maxAmount: 60 })).toEqual([{ label: 'Tapis', amount: 60 }]);
  });

  it('offers nothing when no bet is possible', () => {
    expect(betPresets({ pot: 30, toCall: 10, currentBet: 20, minAmount: 40, maxAmount: 30 })).toEqual([]);
  });
});
