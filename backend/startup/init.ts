import cors from "cors";
import express from "express";
import dbConnection from "./dbConnection.ts";
import setupRouters from "./setupRouters.ts";

const init = (app: express.Application) => {
  app.use(express.json());
  app.use(cors());

  dbConnection();

  setupRouters(app);
};

export default init;
