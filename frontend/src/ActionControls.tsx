export type PokerAction = 'fold' | 'check' | 'call' | 'bet' | 'raise';
type Props = { allowedActions?: PokerAction[]; onAction?: (action: PokerAction) => void };
const actions: PokerAction[] = ['fold', 'check', 'call', 'bet', 'raise'];

export default function ActionControls({ allowedActions = [], onAction }: Props) {
  return (
    <div className="actions" role="group" aria-label="Actions du joueur">
      {actions.map(action => (
        <button key={action} type="button"
          disabled={!onAction || !allowedActions.includes(action) || action === 'bet' || action === 'raise'}
          onClick={() => onAction?.(action)}>
          {action[0].toUpperCase() + action.slice(1)}
        </button>
      ))}
    </div>
  );
}
