export default function PokerTable() {
  return (
    <section className="poker-table" aria-label="Table de Texas Hold’em à deux joueurs">
      <div className="seat"><span aria-hidden="true">🤖</span><strong>Adversaire IA</strong></div>
      <div className="board" aria-hidden="true" />
      <div className="seat"><span aria-hidden="true">👤</span><strong>Vous</strong></div>
    </section>
  );
}
