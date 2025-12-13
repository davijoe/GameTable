import { test, expect } from "@playwright/test";

test("GameGrid loads cards and paginates", async ({ page }) => {
  await page.goto("/");

  //check 1 card exists (loading OR cached)
  const cards = page.getByTestId("game-card");
  await expect(cards.first()).toBeVisible();

  const initialCount = await cards.count();
  expect(initialCount).toBeGreaterThan(0);

  //scroll to start pagination
  await page.evaluate(() => {
    window.scrollTo(0, document.body.scrollHeight);
  });

  // assert that the pagination worked, and there are now more cards
  await expect(async () => {
    const newCount = await cards.count();
    expect(newCount).toBeGreaterThan(initialCount);
  }).toPass();
});