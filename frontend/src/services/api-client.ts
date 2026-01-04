import axios from "axios";
import type { AxiosRequestConfig } from "axios";

export interface PaginatedResponse<T> {
	total: number;
	offset: number;
	limit: number;
	items: T[];
}

const api = axios.create({
	baseURL: import.meta.env.VITE_API_URL,
});

export default class ApiClient<T> {
	private endpoint: string;

	constructor(endpoint: string) {
		this.endpoint = endpoint;
	}

	async getAll(config?: AxiosRequestConfig & { path?: string }) {
		const url = config?.path ? `${this.endpoint}${config.path}` : this.endpoint;
		const res = await api.get<PaginatedResponse<T>>(url, config);
		return res.data;
	}
	async get(id: number | string) {
		const res = await api.get<T>(`${this.endpoint}/${id}`);
		return res.data;
	}

	async create(data: Partial<T>, config?: AxiosRequestConfig) {
		const res = await api.post<T>(this.endpoint, data, config);
		return res.data;
	}

	async update(id: number, data: Partial<T>) {
		const res = await api.put<T>(`${this.endpoint}/${id}`, data);
		return res.data;
	}

	async delete(id: number) {
		const res = await api.delete(`${this.endpoint}/${id}`);
		return res.data;
	}

	async getOne(config?: AxiosRequestConfig): Promise<T> {
		const res = await api.get<T>(this.endpoint, config);
		return res.data;
	}
}
