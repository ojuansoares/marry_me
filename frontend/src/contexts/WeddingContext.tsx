import React, { createContext, useContext, useState, useEffect } from 'react';
import weddingService from '../services/weddingService';
import { useAuth } from './AuthContext';
import authService from '../services/authService';

interface WeddingContextType {
    wedding: any;
    fetchWedding: () => Promise<void>;
    createWedding: (weddingData: WeddingCreate) => Promise<any>;
    deleteWedding: () => Promise<void>;
}

export interface WeddingCreate {
    w_date: string;
    w_location: string;
    w_description: string;
    w_status: string;
}

const WeddingContext = createContext<WeddingContextType | undefined>(undefined);

export function WeddingProvider({ children }: { children: React.ReactNode }) {
    const { userEmail } = useAuth();
    const [wedding, setWedding] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (userEmail) {
            fetchWedding();
        }
    }, [userEmail]);

    const fetchWedding = async () => {
        try {
            setLoading(true);
            const userData = await authService.getCurrentUser();
            const fetchedWedding = await weddingService.getWeddingByFiance(userData.user_id);
            setWedding(fetchedWedding);
        } catch (error) {
            console.error('Erro ao buscar casamento:', error);
        } finally {
            setLoading(false);
        }
    };

    const createWedding = async (weddingData: WeddingCreate) => {
        try {
            const response = await weddingService.createWedding(weddingData);
            setWedding(response);
            console.log('Casamento criado com sucesso:', response);
        } catch (error) {
            console.error('Erro ao criar casamento:', error);
            throw error;
        }
    };

    const deleteWedding = async () => {
        try {
            const userData = await authService.getCurrentUser();
            const fetchedWedding = await weddingService.getWeddingByFiance(userData.user_id);
            await weddingService.deleteWedding(fetchedWedding.id);
            setWedding(null);
        } catch (error) {
            console.error('Erro ao deletar casamento:', error);
        }
    };

    return (
        <WeddingContext.Provider value={{ wedding, fetchWedding, createWedding, deleteWedding }}>
            {children}
        </WeddingContext.Provider>
    );
}

export function useWedding() {
    const context = useContext(WeddingContext);
    if (!context) {
        throw new Error('useWedding deve ser usado dentro de um WeddingProvider');
    }
    return context;
}
