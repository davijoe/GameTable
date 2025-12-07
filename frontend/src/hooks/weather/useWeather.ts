import { useQuery } from "@tanstack/react-query";
import type { Weather } from "../../entities/weather/Weather";
import weatherService from "../../services/weather/weatherService";

export const useWeather = (latitude: number, longitude: number) =>
	useQuery<Weather, Error>({
		queryKey: ["weather", latitude, longitude],
		queryFn: () => weatherService.fetchByGeo({ latitude, longitude }),
	});