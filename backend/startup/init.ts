import cors from "cors";
import express from "express";
import dbConnection from "./dbConnection";
import setupRouters from "./setupRouters";

const init = (app: express.Application) => {
  app.use(express.json());
  app.use(cors());

  dbConnection();

  setupRouters(app);
};

export default init;
