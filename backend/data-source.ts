import "reflect-metadata";
import "dotenv/config";
import { DataSource } from "typeorm";
import { Game } from "./entity/Game.ts";
import { Genre } from "./entity/Genre.ts";


export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.DB_HOST || "127.0.0.1", 
  port: Number(process.env.DB_PORT || 3037),
  username: process.env.DB_USERNAME || "root",
  password: process.env.DB_PASSWORD || "123456",
  database: process.env.DB_NAME || "gametable",
  entities: [Game, Genre],
  synchronize: true,
  logging: true,
  timezone: "Z"
});
