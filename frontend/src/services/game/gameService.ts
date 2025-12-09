import type { Game } from "../../entities/Game";
import ApiClient from "../api-client";

const gameService = new ApiClient<Game>("/games");

export default gameService;