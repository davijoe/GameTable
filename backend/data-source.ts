import "dotenv/config";
import { DataSource } from "typeorm";
import { Game } from "./entity/Game";
import { Genre } from "./entity/Genre";

//const DB_TYPE = (process.env.DB_TYPE) as "mysql";
//const DB_HOST = process.env.DB_HOST ?? "127.0.0.1";
//const DB_PORT = Number(process.env.DB_PORT ?? 3307);
//const DB_USERNAME = process.env.DB_USERNAME ?? "app";
//const DB_PASSWORD = process.env.DB_PASSWORD ?? "changeme";
//const DB_NAME = process.env.DB_NAME ?? "gametable";
const DB_TYPE = process.env.DB_TYPE;
const DB_HOST = process.env.DB_HOST;
const DB_PORT = Number(process.env.DB_PORT);
const DB_USERNAME = process.env.DB_USERNAME;
const DB_PASSWORD = process.env.DB_PASSWORD;
const DB_NAME = process.env.DB_NAME;

console.log("[DB] Type:", DB_TYPE, "| Name:", DB_NAME);
console.log("[DB] Host:", DB_HOST, "| Port:", DB_PORT);
console.log("[DB] Username:", DB_USERNAME, "| Password:", DB_PASSWORD);

// Quick validation before constructing the DataSource
if (!Number.isFinite(DB_PORT)) throw new Error(`Invalid DB_PORT: ${process.env.DB_PORT}`);
if (!DB_HOST) throw new Error("DB_HOST is required");
if (!DB_USERNAME) throw new Error("DB_USERNAME is required");
if (DB_PASSWORD == null) throw new Error("DB_PASSWORD is required");
if (!DB_NAME) throw new Error("DB_NAME is required");

export const AppDataSource = new DataSource({
  type: DB_TYPE,
  host: DB_HOST,
  port: DB_PORT,
  username: DB_USERNAME,
  password: DB_PASSWORD,
  database: DB_NAME,
  entities: [Game, Genre],
  synchronize: true,
  logging: true
});
