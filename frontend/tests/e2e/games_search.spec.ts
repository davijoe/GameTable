import { test, expect } from "@playwright/test";

const SEARCH_TERM = "Catan";

test("game search filter - test 3 games contain search term", async ({
  page,
}) => {
  await page.goto("/");

  const cards = page.getByTestId("game-card");

  // Wait for initial load (cached or fresh)
  await expect(cards.first()).toBeVisible();

  await page.getByTestId("game-search-bar").fill(SEARCH_TERM);

  // wait for request
  await page.waitForResponse(
    (resp) =>
      resp.url().includes("/api/games") &&
      resp.url().includes(`q=${encodeURIComponent(SEARCH_TERM)}`) &&
      resp.ok()
  );

  // assert results are rendered
  await expect(cards.nth(0)).toBeVisible();
  await expect(cards.nth(1)).toBeVisible();
  await expect(cards.nth(2)).toBeVisible();

  // assert first 3 cards contain the search term
  await expect(cards.nth(0)).toContainText(SEARCH_TERM);
  await expect(cards.nth(1)).toContainText(SEARCH_TERM);
  await expect(cards.nth(2)).toContainText(SEARCH_TERM);
});
