import { Router } from "express";
import { Game } from "../entity/Game";
import { getGames } from "../service/gameService";

interface Response {
  count: number;
  results: ModifiedGame[];
}

const gameRouter = Router();

gameRouter.get("/", async (req, res) => {
  const games = await getGames(req); // Fetching games using the service layer

  const response: Response = {
    count: games.length,
    results: games,
  }
  res.send(response); // Sending the response back to the client
});

export default gameRouter;
