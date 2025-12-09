import type { GameDetail } from "../../entities/GameDetail";
import ApiClient from "../api-client";

const gameDetailService = new ApiClient<GameDetail>("/games");

export default gameDetailService;