import { AppDataSource } from "../data-source.ts";

const dbConnection = async () => {
  try {
    await AppDataSource.initialize();
    console.log("Data Source has been initialized!");
  } catch (err) {
    console.error("Error during Data Source initialization:", err);
  }
};

export default dbConnection;
