import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_URL } from '@env';
const WEDDING_URL = `${API_URL}/weddings`;

export interface WeddingCreate {
    w_date: string;
    w_location: string;
    w_description: string;
    w_status: string;
}

class WeddingService {
    async createWedding(weddingData: WeddingCreate): Promise<any> {
        try {
            const token = await AsyncStorage.getItem('token');
            if (!token) throw new Error('Usuário não autenticado');

            const response = await axios.post(`${WEDDING_URL}/`, weddingData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            console.log("Dados enviados:", weddingData);
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

            const response = await axios.get(`${WEDDING_URL}/fiance/${fianceId}`, {
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
            const token = await AsyncStorage.getItem('token');
            if (!token) throw new Error('Usuário não autenticado');

            const response = axios.delete(`${WEDDING_URL}/${weddingId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            return (await response).data;
        } catch (error) {
            console.error('Error deleting wedding:', error);
            throw error;
        }
    }
}

export default new WeddingService();
