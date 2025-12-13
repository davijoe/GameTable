import { test, expect } from '@playwright/test';

//checks that homepage loads and title is "Game Table"
test('homepage loads', async ({ page }) => {
	await page.goto('/');

	await expect(page).toHaveTitle(/Game Table/i);
});
