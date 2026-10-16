export type BetPreset = { label: string; amount: number };
export type SizingInput = { pot: number; toCall: number; currentBet: number; minAmount: number; maxAmount: number };

const fractions = [
  { label: '½ pot', share: 0.5 },
  { label: '¾ pot', share: 0.75 },
  { label: 'Pot', share: 1 },
];

export function clampAmount(amount: number, minAmount: number, maxAmount: number): number {
  return Math.min(Math.max(Math.round(amount), minAmount), maxAmount);
}

export function potSizedTarget(share: number, { pot, toCall, currentBet }: Pick<SizingInput, 'pot' | 'toCall' | 'currentBet'>): number {
  return currentBet + share * (pot + toCall);
}

export function betPresets(input: SizingInput): BetPreset[] {
  const { minAmount, maxAmount } = input;
  if (maxAmount < minAmount) return [];
  if (maxAmount === minAmount) return [{ label: 'Tapis', amount: maxAmount }];
  const presets: BetPreset[] = [{ label: 'Min', amount: minAmount }];
  for (const { label, share } of fractions) {
    const amount = clampAmount(potSizedTarget(share, input), minAmount, maxAmount);
    if (amount > minAmount && amount < maxAmount) presets.push({ label, amount });
  }
  presets.push({ label: 'Tapis', amount: maxAmount });
  return presets.filter((preset, index) => presets.findIndex(other => other.amount === preset.amount) === index);
}
