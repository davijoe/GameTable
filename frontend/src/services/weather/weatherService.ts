import ApiClient from "../api-client";
import type { Weather } from "../../entities/weather/Weather";

class WeatherService extends ApiClient<Weather> {
	async fetchByGeo(params: { latitude: number; longitude: number }): Promise<Weather> {
		return this.getOne({ params });
	}
}

const weatherService = new WeatherService("/weather/geo");
export default weatherService;