const formatter = new Intl.NumberFormat('fr-FR');

export default function ChipAmount({ amount }: { amount?: number }) {
  return <span>{amount === undefined ? '—' : `${formatter.format(amount)} jetons`}</span>;
}
