import { test as base, expect } from "@playwright/test";
import dotenv from "dotenv";

//quiet to not print in console
dotenv.config({ quiet: true });

export const test = base.extend<{
  apiBase: string;
  adminUser: string;
  adminPassword: string;
}>({
  apiBase: [process.env.E2E_BACKEND_PATH!, { scope: "test" }],
  adminUser: [process.env.E2E_ADMIN_USERNAME!, { scope: "test" }],
  adminPassword: [process.env.E2E_ADMIN_PASSWORD!, { scope: "test" }],
});

export { expect };
