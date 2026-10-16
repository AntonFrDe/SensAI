import { expect, test, type Page } from '@playwright/test';

test.beforeEach(async ({ page }, testInfo) => {
  if (!testInfo.title.includes('guided tour')) {
    await page.addInitScript(() => localStorage.setItem('sensai-tour-done', 'true'));
  }
});

async function startGame(page: Page) {
  await page.goto('/');
  await page.getByRole('button', { name: 'Jouer' }).click();
  await expect(page.getByText('Tour : à vous de jouer')).toBeVisible();
}

test('plays a hand against the opponent and keeps it in the history', async ({ page }) => {
  await startGame(page);
  await expect(page.getByText('L’IA suit.')).toBeVisible();
  await page.getByRole('button', { name: 'Check' }).click();
  await expect(page.getByText('Phase : Flop')).toBeVisible();
  await expect(page.getByLabel(/^Votre main :/)).toBeVisible();

  await expect(page.getByRole('button', { name: 'Fold' })).toBeEnabled();
  await page.getByRole('button', { name: 'Fold' }).click();
  await expect(page.getByText(/L’IA remporte \d+ jetons \(adversaire couché\)\./)).toBeVisible();
  await expect(page.getByRole('region', { name: 'Statistiques' })).toContainText('Mains jouées1');
  await expect(page.getByRole('region', { name: 'Mains précédentes' }).getByRole('listitem')).toHaveCount(1);

  const stats = page.getByRole('region', { name: 'Statistiques' });
  await stats.getByRole('textbox', { name: 'Ce que je retiens (facultatif)' }).fill('Je me couche trop vite.');
  await stats.getByRole('button', { name: 'Ajouter à mes notes' }).click();
  await expect(stats.getByRole('status')).toContainText(/partie web, 1 main, 0 gagnée, bilan -\d+ jetons\. Je me couche trop vite\./);

  await page.getByRole('button', { name: 'Main suivante' }).click();
  await expect(page.getByText('Phase : Préflop')).toBeVisible();
});

test('plays with the keyboard and a bet preset', async ({ page }) => {
  await startGame(page);
  await expect(page.getByRole('button', { name: 'Check' })).toBeEnabled();
  await page.keyboard.press('t');
  await expect(page.getByRole('spinbutton', { name: 'Montant total (Bet / Raise)' })).not.toHaveValue('');
  await page.keyboard.press('r');
  await expect(page.locator('.action-bubble').filter({ hasText: /^Relance à/ })).toBeVisible();
});

test('streams the coach advice and answers a follow-up question', async ({ page }) => {
  await startGame(page);
  const coach = page.getByRole('complementary', { name: 'Coach SensAI' });
  await coach.getByRole('button', { name: 'Demander conseil' }).click();
  await expect(coach.getByText('Hello')).toBeVisible();
  await coach.getByRole('button', { name: 'Et si je relance ?' }).click();
  await expect(coach.getByRole('listitem')).toHaveCount(3);
  await expect(coach.getByRole('listitem').last()).toContainText('Hello');
});

test('computes the odds of the current decision', async ({ page }) => {
  await startGame(page);
  const odds = page.getByRole('region', { name: 'Repères chiffrés' });
  await odds.getByRole('button', { name: 'Afficher mes repères' }).click();
  await expect(odds.getByRole('meter', { name: 'Équité' })).toBeVisible();
  await expect(odds).toContainText('contre une main au hasard');
});

test('resumes the game after a reload', async ({ page }) => {
  await startGame(page);
  const cards = await page.getByRole('group', { name: 'Vos cartes privées' }).first().textContent() ?? '';
  await page.reload();
  await page.getByRole('button', { name: 'Reprendre la partie' }).click();
  await expect(page.getByRole('group', { name: 'Vos cartes privées' }).first()).toHaveText(cards);
});

test('finds a term in the glossary and shows the hand rankings', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('region', { name: 'État des modèles' })).toContainText('Coach : ok installé');
  await page.getByRole('button', { name: 'Glossaire' }).click();
  await page.getByRole('searchbox', { name: 'Chercher un terme' }).fill('kicker');
  await expect(page.getByText(/Carte accompagnant/)).toBeVisible();
  await page.getByRole('button', { name: '← Accueil' }).click();
  await page.getByRole('button', { name: 'Classement des mains' }).click();
  await expect(page.getByRole('listitem')).toHaveCount(10);
});

test('shows the guided tour on the first game', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Jouer' }).click();
  const tour = page.getByRole('dialog');
  await expect(tour).toContainText('Vos cartes et le board');
  await expect(page.locator('.tour-target')).toHaveCount(1);
  for (let step = 0; step < 3; step++) await tour.getByRole('button', { name: 'Suivant' }).click();
  await tour.getByRole('button', { name: 'Terminer' }).click();
  await page.reload();
  await page.getByRole('button', { name: 'Reprendre la partie' }).click();
  await expect(page.getByRole('dialog')).toHaveCount(0);
});

