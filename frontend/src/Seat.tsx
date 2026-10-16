import type { ReactNode } from 'react';
import ChipAmount from './ChipAmount';
import Term from './Term';

export type SeatData = {
  name: string;
  stack: number;
  bet: number;
  folded: boolean;
  allIn: boolean;
  dealer: boolean;
  blind: 'small' | 'big' | null;
};
export type SeatProps = {
  seat?: SeatData;
  label: string;
  avatar: string;
  active?: boolean;
  position: 'top' | 'bottom';
  children?: ReactNode;
};

const blindLabels = { small: 'Petite blinde', big: 'Grosse blinde' };
const blindShort = { small: 'SB', big: 'BB' };

export default function Seat({ seat, label, avatar, active = false, position, children }: SeatProps) {
  const classes = ['seat-box', position, active ? 'active' : '', seat?.folded ? 'folded' : ''].filter(Boolean).join(' ');
  return (
    <section className={classes} aria-label={label} aria-current={active ? 'true' : undefined}>
      <div className="seat-head">
        <span className="avatar" aria-hidden="true">{avatar}</span>
        <strong>{label}</strong>
        {seat?.dealer && <span className="dealer-button" title="Donneur" aria-label="Donneur">D</span>}
        {seat?.blind && <span className="role-badge" title={blindLabels[seat.blind]} aria-label={blindLabels[seat.blind]}>
          {blindShort[seat.blind]}
        </span>}
      </div>
      <p className="chip-info"><Term term="stack">Stack</Term> : <ChipAmount amount={seat?.stack} /></p>
      {children}
      <p className="seat-status" aria-live="polite">
        {seat?.folded ? 'Couché' : seat?.allIn ? 'Tapis' : active ? 'Doit jouer' : ''}
      </p>
      {seat !== undefined && seat.bet > 0 && <p className="bet-chip">Mise : <ChipAmount amount={seat.bet} /></p>}
    </section>
  );
}
