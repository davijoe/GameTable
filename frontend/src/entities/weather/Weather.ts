export interface Weather {
	hourly: {
		time: string[];
		temperature_2m: number[];
	};
}