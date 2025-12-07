import { Box, Text, Spinner } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

type WeatherResponse = {
  hourly: {
    time: string[];
    temperature_2m: number[];
  };
};

const fetchWeather = async (): Promise<WeatherResponse> => {
  const res = await fetch(
    "/http://localhost:8000/api/weather/geo?latitude=55.6759&longitude=12.5655"
  );
  if (!res.ok) throw new Error("Failed to fetch weather");
  return res.json();
};

export default function WeatherTab() {
  const { data, isLoading, error } = useQuery<WeatherResponse, Error, WeatherResponse>({
    queryKey: ["weather"],
    queryFn: fetchWeather,
  });

  if (isLoading) return <Spinner />;
  if (error) return <Text color="red.500">{error.message}</Text>;

  // transform API response into array of {time, temp}
  const chartData = data!.hourly.time.map((t, i) => ({
    time: t.split("T")[1], // just the hour
    temp: data!.hourly.temperature_2m[i],
  }));

  return (
    <Box w="100%" h="400px">
      <Text fontSize="xl" mb={2}>Hourly Temperature (°C)</Text>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <XAxis dataKey="time" />
          <YAxis unit="°C" />
          <Tooltip />
          <Line type="monotone" dataKey="temp" stroke="#3182CE" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
}