import express from "express";
import init from "./startup/init";

const app = express();

init(app);

app.get("/health", async (_req, res) => {
  let dbStatus = "down";

  try {
    console.log("Checking database connection...");
    await AppDataSource.query("SELECT 1");
    dbStatus = "ok";
  } catch {
    console.error("Database connection failed");
    dbStatus = "down";
  }

  res.status(dbStatus === "ok" ? 200 : 500).json({
    server: "ok",
    db: dbStatus,
  });
});

app.get("/", (req, res) => {
  res.send("Hello, World!");
});

app.listen(8000, () => {
  console.log("Server is running on http://localhost:8000");
});
