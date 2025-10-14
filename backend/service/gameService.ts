import { SelectQueryBuilder } from "typeorm";
import { AppDataSource } from "../data-source";
import { Game } from "../entity/Game";
import { ModifiedGame } from "../router/gameRouter";

const gameRepository = AppDataSource.getRepository(Game);


const toNum = (v: unknown): number | undefined => {
  const n = Number(v);
  return Number.isFinite(n) ? n : undefined;
};

const toBool = (v: unknown): boolean | undefined => {
  if (v === undefined || v === null) return undefined;
  const s = String(v).trim().toLowerCase();
  if (["1", "true", "t", "yes", "y"].includes(s)) return true;
  if (["0", "false", "f", "no", "n"].includes(s)) return false;
  return undefined;
};

const addGenreFilter = (qb: SelectQueryBuilder<Game>, genreId?: number) => {
  if (genreId != null) {
    // Fast EXISTS against the join table defined in @JoinTable({ name: "game_genres", ... })
    qb.andWhere(
      `EXISTS (
         SELECT 1 FROM game_genres gg
         WHERE gg.game_id = game.id
           AND gg.genre_id = :genreId
       )`,
      { genreId }
    );
  }
};

const addAvailableFilter = (qb: SelectQueryBuilder<Game>, available?: boolean) => {
  if (available != null) qb.andWhere("game.available = :available", { available });
};

const addPlayersFilter = (
  qb: SelectQueryBuilder<Game>,
  minPlayers?: number,
  maxPlayers?: number
) => {
  if (minPlayers != null) qb.andWhere("game.minPlayers >= :minPlayers", { minPlayers });
  if (maxPlayers != null) qb.andWhere("game.maxPlayers <= :maxPlayers", { maxPlayers });
};

const addPlayTimeFilter = (
  qb: SelectQueryBuilder<Game>,
  playTimeMin?: number,
  playTimeMax?: number
) => {
  if (playTimeMin != null) qb.andWhere("game.playTime >= :playTimeMin", { playTimeMin });
  if (playTimeMax != null) qb.andWhere("game.playTime <= :playTimeMax", { playTimeMax });
};

const addYearFilter = (
  qb: SelectQueryBuilder<Game>,
  yearMin?: number,
  yearMax?: number
) => {
  // yearPublished is varchar(5) in your entity. Cast to unsigned for range filters.
  if (yearMin != null) qb.andWhere("CAST(game.yearPublished AS UNSIGNED) >= :yearMin", { yearMin });
  if (yearMax != null) qb.andWhere("CAST(game.yearPublished AS UNSIGNED) <= :yearMax", { yearMax });
};

const addSearch = (qb: SelectQueryBuilder<Game>, search?: string) => {
  if (search) {
    // Assuming case-insensitive collation on `name`
    qb.andWhere("game.name LIKE :search", { search: `%${search}%` });
  }
};

const ORDER_MAP: Record<string, [string, "ASC" | "DESC"]> = {
  "name": ["game.name", "ASC"],
  "-name": ["game.name", "DESC"],
  "bggRating": ["game.bggRating", "ASC"],
  "-bggRating": ["game.bggRating", "DESC"],
  "difficultyRating": ["game.difficultyRating", "ASC"],
  "-difficultyRating": ["game.difficultyRating", "DESC"],
  "playTime": ["game.playTime", "ASC"],
  "-playTime": ["game.playTime", "DESC"],
  "year": ["CAST(game.yearPublished AS UNSIGNED)", "ASC"],
  "-year": ["CAST(game.yearPublished AS UNSIGNED)", "DESC"],
};

const addOrdering = (qb: SelectQueryBuilder<Game>, ordering?: string) => {
  const [col, dir] = ORDER_MAP[ordering ?? ""] ?? ["game.bggRating", "DESC"];
  qb.orderBy(col, dir);
};

// If you want to reshape, do it here. For now pass-through.
const modifyGameResponse = (games: Game[]): ModifiedGame[] => games as unknown as ModifiedGame[];

// ---------- main ----------
export const getGames = async (req: any): Promise<ModifiedGame[]> => {
  // parse query
  const genreId = toNum(req.query.genres);
  const available = toBool(req.query.available);
  const search = typeof req.query.search === "string" ? req.query.search.trim() : undefined;
  const ordering = typeof req.query.ordering === "string" ? req.query.ordering : undefined;

  const minPlayers = toNum(req.query.minPlayers);
  const maxPlayers = toNum(req.query.maxPlayers);
  const playTimeMin = toNum(req.query.playTimeMin);
  const playTimeMax = toNum(req.query.playTimeMax);
  const yearMin = toNum(req.query.yearMin);
  const yearMax = toNum(req.query.yearMax);

  // pagination
  const page = Math.max(1, Number(req.query.page) || 1);
  const pageSize = Math.min(100, Math.max(1, Number(req.query.pageSize) || 20));
  const offset = (page - 1) * pageSize;

  // query
  const qb = gameRepository
    .createQueryBuilder("game")
    .leftJoinAndSelect("game.genres", "genres") // include genres in results
    .distinct(true);

  addGenreFilter(qb, genreId);
  addAvailableFilter(qb, available);
  addPlayersFilter(qb, minPlayers, maxPlayers);
  addPlayTimeFilter(qb, playTimeMin, playTimeMax);
  addYearFilter(qb, yearMin, yearMax);
  addSearch(qb, search);
  addOrdering(qb, ordering);

  const games = await qb.skip(offset).take(pageSize).getMany();
  return modifyGameResponse(games);
};
