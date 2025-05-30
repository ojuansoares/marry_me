import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_URL } from '@env';
const AUTH_URL = `${API_URL}/auth`;;  // Substitua pelo seu IP local

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user_type: string;
    user_email: string;
    user_id: number;
}

export interface UserCreate {
    u_name: string;
    u_email: string;
    u_phone: string;
    u_type: string; // 'fiance' ou 'guest'
    u_password: string;
}

class AuthService {
    async login(credentials: LoginCredentials): Promise<AuthResponse> {
        try {
            console.log('Attempting login to:', `${AUTH_URL}/login`);
            // Criar FormData para enviar os dados no formato correto do OAuth2
            const formData = new URLSearchParams();
            formData.append('username', credentials.username);
            formData.append('password', credentials.password);

            const response = await axios.post(`${AUTH_URL}/login`, formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json',
                }
            });
            console.log('Login response received:', response.data);
            if (response.data.access_token) {
                await AsyncStorage.setItem('token', response.data.access_token);
                await AsyncStorage.setItem('user', JSON.stringify(response.data));
            }
            return response.data;
        } catch (error) {
            console.error('Login error:', error);
            if (axios.isAxiosError(error)) {
                console.error('Response data:', error.response?.data);
                console.error('Response status:', error.response?.status);
                console.error('Response headers:', error.response?.headers);
                if (error.code === 'ECONNREFUSED') {
                    throw new Error('Não foi possível conectar ao servidor. Verifique se o backend está rodando.');
                }
                if (error.response?.status === 422) {
                    throw new Error('Dados de login inválidos. Verifique o formato dos dados.');
                }
                throw new Error(error.response?.data?.detail || 'Erro ao fazer login');
            }
            throw error;
        }
    }

    async createUser(userData: UserCreate): Promise<void> {
        try {
            console.log('Creating user with data:', userData);
            await axios.post(`${API_URL}/users/`, userData); // Endpoint para criar usuário
        } catch (error) {
            console.error('Error creating user:', error);
            throw error;
        }
    }

    async logout(): Promise<void> {
        await AsyncStorage.removeItem('token');
        await AsyncStorage.removeItem('user');
    }

    async getCurrentToken(): Promise<string | null> {
        return await AsyncStorage.getItem('token');
    }

    async getCurrentUser(): Promise<AuthResponse> {
        const userStr = await AsyncStorage.getItem('user');
        if (!userStr) {
            throw new Error('No user data found');
        }
        return JSON.parse(userStr);
    }

    async isAuthenticated(): Promise<boolean> {
        const token = await this.getCurrentToken();
        return !!token;
    }

    async testConnection(): Promise<boolean> {
        try {
            console.log('Testing connection to:', `${API_URL}/auth/test`);
            const response = await axios.get(`${AUTH_URL}/test`);
            console.log('Test response:', response.data);
            return true;
        } catch (error) {
            console.error('Connection test failed:', error);
            if (axios.isAxiosError(error)) {
                console.error('Error details:', {
                    code: error.code,
                    message: error.message,
                    response: error.response?.data
                });
            }
            return false;
        }
    }
}

export default new AuthService(); 