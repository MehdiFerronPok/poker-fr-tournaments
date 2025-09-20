import { test, expect } from '@playwright/test';

test('homepage has title and search input', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.getByText('Tournois de poker France')).toBeVisible();
  await expect(page.getByPlaceholder('Ville (optionnel)')).toBeVisible();
});