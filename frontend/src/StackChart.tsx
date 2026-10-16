import { useState, type KeyboardEvent, type PointerEvent } from 'react';
import type { StackPoint } from './handLog';

export type StackChartProps = { points: StackPoint[]; title: string };

const width = 320;
const height = 160;
const pad = { left: 44, right: 56, top: 12, bottom: 22 };
const formatter = new Intl.NumberFormat('fr-FR');

export function niceTicks(min: number, max: number): number[] {
  const range = max - min || Math.max(Math.abs(max) * 0.1, 10);
  const raw = range / 3;
  const power = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 5, 10].map(multiple => multiple * power).find(candidate => candidate >= raw) ?? raw;
  const ticks: number[] = [];
  for (let tick = Math.floor(min / step) * step; tick <= Math.ceil(max / step) * step; tick += step) ticks.push(tick);
  return ticks.length > 1 ? ticks : [ticks[0] - step, ticks[0], ticks[0] + step];
}

function handLabel(hand: number): string {
  return hand === 0 ? 'Départ' : `Main n°${hand}`;
}

export default function StackChart({ points, title }: StackChartProps) {
  const [active, setActive] = useState<number | null>(null);
  if (points.length < 2) return null;
  const stacks = points.map(point => point.stack);
  const ticks = niceTicks(Math.min(...stacks), Math.max(...stacks));
  const [low, high] = [ticks[0], ticks[ticks.length - 1]];
  const x = (index: number) => pad.left + (index / (points.length - 1)) * (width - pad.left - pad.right);
  const y = (stack: number) => pad.top + (1 - (stack - low) / (high - low)) * (height - pad.top - pad.bottom);
  const line = points.map((point, index) => `${index ? 'L' : 'M'}${x(index).toFixed(1)},${y(point.stack).toFixed(1)}`).join(' ');
  const area = `${line} L${x(points.length - 1).toFixed(1)},${height - pad.bottom} L${pad.left},${height - pad.bottom} Z`;
  const last = points.length - 1;
  const shown = active === null ? null : points[active];

  function onPointerMove(event: PointerEvent<SVGSVGElement>) {
    const box = event.currentTarget.getBoundingClientRect();
    const ratio = ((event.clientX - box.left) / box.width * width - pad.left) / (width - pad.left - pad.right);
    setActive(Math.min(Math.max(Math.round(ratio * last), 0), last));
  }

  function onKeyDown(event: KeyboardEvent<SVGSVGElement>) {
    const moves: Record<string, number> = { ArrowLeft: -1, ArrowRight: 1 };
    if (!(event.key in moves)) return;
    event.preventDefault();
    setActive(current => Math.min(Math.max((current ?? last) + moves[event.key], 0), last));
  }

  return (
    <figure className="stack-chart">
      <figcaption>{title}</figcaption>
      <div className="chart-frame">
        <svg viewBox={`0 0 ${width} ${height}`} role="img" tabIndex={0}
          aria-label={`${title} : de ${formatter.format(points[0].stack)} à ${formatter.format(points[last].stack)} jetons en ${last} main${last > 1 ? 's' : ''}.`}
          onPointerMove={onPointerMove} onPointerLeave={() => setActive(null)} onFocus={() => setActive(last)}
          onBlur={() => setActive(null)} onKeyDown={onKeyDown}>
          {ticks.map(tick => <g key={tick}>
            <line className="chart-grid" x1={pad.left} x2={width - pad.right} y1={y(tick)} y2={y(tick)} />
            <text className="chart-axis" x={pad.left - 6} y={y(tick)} textAnchor="end" dominantBaseline="middle">{formatter.format(tick)}</text>
          </g>)}
          <line className="chart-reference" x1={pad.left} x2={width - pad.right} y1={y(points[0].stack)} y2={y(points[0].stack)} />
          <path className="chart-area" d={area} />
          <path className="chart-line" d={line} />
          <text className="chart-axis" x={pad.left} y={height - 6} textAnchor="start">{handLabel(points[0].hand)}</text>
          <text className="chart-axis" x={x(last)} y={height - 6} textAnchor="end">{handLabel(points[last].hand)}</text>
          {shown && active !== null && <line className="chart-crosshair" x1={x(active)} x2={x(active)} y1={pad.top} y2={height - pad.bottom} />}
          <circle className="chart-dot" cx={x(active ?? last)} cy={y(points[active ?? last].stack)} r={4} />
          <text className="chart-end" x={x(last) + 8} y={y(points[last].stack)} dominantBaseline="middle">{formatter.format(points[last].stack)}</text>
        </svg>
        {shown && active !== null && <div className="chart-tooltip" role="status"
          style={{ left: `${(x(active) / width) * 100}%`, top: `${(y(shown.stack) / height) * 100}%` }}>
          <strong>{formatter.format(shown.stack)} jetons</strong>
          <span>{handLabel(shown.hand)}</span>
        </div>}
      </div>
      <details className="chart-table">
        <summary>Voir les valeurs</summary>
        <table>
          <thead><tr><th scope="col">Moment</th><th scope="col">Votre tapis</th></tr></thead>
          <tbody>{points.map(point => <tr key={point.hand}><td>{handLabel(point.hand)}</td><td>{formatter.format(point.stack)}</td></tr>)}</tbody>
        </table>
      </details>
    </figure>
  );
}
