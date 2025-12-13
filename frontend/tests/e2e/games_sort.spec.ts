import { test, expect } from "@playwright/test";


const SORT_FIELDS = [
	{ label: "Rating", value: "bgg_rating", testId: "game-rating" },
	{ label: "Year Published", value: "year_published", testId: "game-year" },
	{ label: "Playing Time", value: "playing_time", testId: "game-playing-time" },
];

for (const { label, value, testId } of SORT_FIELDS) {
	test(`GameGrid sort by ${label} and toggle`, async ({ page }) => {
		await page.goto("/");

		const firstCard = page.getByTestId("game-card").first();
		const valueLocator = firstCard.getByTestId(testId);

		// save first card value before sorting
		const valueBefore = await valueLocator.textContent();

		// select sort option and click toggle
		await page.getByTestId("games_sort_select").selectOption(value);
		await page.getByTestId("games-sort-toggle-button").click();
		await page.waitForTimeout(500); // wait for cards to re-render

		// first card value should change after sort
		const valueAfterSort = await valueLocator.textContent();
		expect(valueAfterSort).not.toEqual(valueBefore);

		// click toggle button again to reverse sort order
		await page.getByTestId("games-sort-toggle-button").click();
		await page.waitForTimeout(500);

		// first card value should change again after toggle
		const valueAfterToggle = await valueLocator.textContent();
		expect(valueAfterToggle).not.toEqual(valueAfterSort);
	});
}