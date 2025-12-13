import { test, expect} from "../fixtures/env_loader_fixture.ts";

//randomness so test is not so flaky with other tests running same time
const timestamp = Date.now();
const random = Math.floor(Math.random() * 10000);

const NEW_USER_TEST_DISPLAYNAME = `e2e test user ${random}`;
const NEW_USER_TEST_USERNAME = `e2e_username_${timestamp}_${random}`;
const NEW_USER_TEST_PASSWORD = "e2e test password";
const NEW_USER_TEST_EMAIL = `e2e_${timestamp}_${random}@mail.com`;
const NEW_USER_TEST_DOB = "1999-10-30";

let created_user_id : number

test("register new user", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Login" }).click();
  await page.getByText("Need an account? Sign up").click();

  await page.getByRole("textbox", { name: "Display Name" }).fill(NEW_USER_TEST_DISPLAYNAME);
  await page.getByRole("textbox", { name: "Email" }).fill(NEW_USER_TEST_EMAIL);
  await page.getByRole("textbox", { name: "Date of Birth" }).fill(NEW_USER_TEST_DOB);
  await page.getByRole("textbox", { name: "Username" }).fill(NEW_USER_TEST_USERNAME);
  await page.getByRole("textbox", { name: "Password" }).fill(NEW_USER_TEST_PASSWORD);

  // subscribe to api call to get user id
  const [response] = await Promise.all([
    page.waitForResponse(resp =>
      resp.url().endsWith("/api/users") &&
      resp.request().method() === "POST"
    ),
    page.getByRole("button", { name: "Create Account" }).click(),
  ]);

  const newUser = await response.json();
  created_user_id = newUser.id; // save id for next delete test

  await page.waitForTimeout(1000);

  // navigate to Profile page and assert
  await page.getByRole("link", { name: "Profile" }).click();
  await expect(page.getByText(NEW_USER_TEST_DISPLAYNAME)).toBeVisible();
  await expect(page.getByText(NEW_USER_TEST_USERNAME)).toBeVisible();
  await expect(page.getByText(NEW_USER_TEST_EMAIL)).toBeVisible();
});

test('delete user', async ({request, apiBase, adminUser, adminPassword }) => {
    const loginRes = await request.post(`${apiBase}/auth/login`, {
        data: {
            username: adminUser,
            password: adminPassword,
        },
    });
    expect(loginRes.ok()).toBeTruthy();

    const { access_token } = await loginRes.json();
    expect(access_token).toBeTruthy();
    
    // delete the user
    const deleteRes = await request.delete(`${apiBase}/api/user/${created_user_id}`, {
        headers: {
            Authorization: `Bearer ${access_token}`,
        },
    });

    expect(deleteRes.status()).toBe(204);
});



