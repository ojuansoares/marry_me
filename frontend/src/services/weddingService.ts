import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'http://192.168.230.139:8000/weddings'; // Substitua pelo seu IP local

export interface WeddingCreate {
    w_date: string;
    w_location: string;
    w_description: string;
    w_status: string;
}

class WeddingService {
    async createWedding(weddingData: WeddingCreate): Promise<void> {
        try {
            const token = await AsyncStorage.getItem('token');
            if (!token) throw new Error('Usuário não autenticado');

            const response = await axios.post(`${API_URL}/`, weddingData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            return response.data;
        } catch (error) {
            console.error('Erro ao criar casamento:', error);
            throw error;
        }
    }

    async getWeddingByFiance(fianceId: number) {
        try {
            const token = await AsyncStorage.getItem('token');
            if (!token) throw new Error('Usuário não autenticado');

            const response = await axios.get(`${API_URL}/fiance/${fianceId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            return response.data;
        } catch (error) {
            console.error('Erro ao buscar casamento:', error);
            throw error;
        }
    }

    async deleteWedding(weddingId: number): Promise<void> {
        try {
            await axios.delete(`${API_URL}/${weddingId}`);
        } catch (error) {
            console.error('Error deleting wedding:', error);
            throw error;
        }
    }
}

export default new WeddingService();
