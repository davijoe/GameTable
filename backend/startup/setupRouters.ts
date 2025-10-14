import express from "express"
import gameRouter from "../router/gameRouter.ts";
// import genreRouter from "../router/genreRouter.ts";

const setupRouters = (app: express.Application) => {
  app.use("/games", gameRouter);
};

export default setupRouters;
