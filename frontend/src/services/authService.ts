import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Use seu IP local aqui
const API_URL = 'http://192.168.3.18:8000';  // IP correto da sua máquina

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user_type: string;  // Adicionando user_type
}

class AuthService {
    async login(credentials: LoginCredentials): Promise<AuthResponse> {
        try {
            const response = await axios.post(`${API_URL}/auth/login`, credentials, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
            });
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
                throw new Error(error.response?.data?.detail || 'Erro ao fazer login');
            }
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
}

export default new AuthService(); 