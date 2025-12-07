import { Box, Text, Spinner } from "@chakra-ui/react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { useWeather } from "../../hooks/weather/useWeather";

export default function WeatherTab() {
	const { data, isLoading, error } = useWeather(55.69322257328163, 12.553167082799739); //copenhagen

	if (isLoading) return <Spinner />;
	if (error) return <Text color="red.500">Something went wrong getting the weather</Text>;

  //map the data into array
	const chartData = data!.hourly.time.map((t, i) => ({
		time: t.split("T")[1], // "HH:MM"
		temp: data!.hourly.temperature_2m[i],
	}));

	return (
		<Box w="100%" h="400px">
			<Text fontSize="xl" mb={2}>
				Hourly Temperature at EK Guldbergsgade (°C)
			</Text>
			<ResponsiveContainer width="100%" height="100%">
				<LineChart data={chartData}>
					<XAxis dataKey="time" />
					<YAxis unit="°C" />
					<Tooltip />
					<Line dataKey="temp" stroke="#3182CE" strokeWidth={2} />
				</LineChart>
			</ResponsiveContainer>
		</Box>
	);
}