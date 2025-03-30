import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import authService from '../services/authService';

interface AuthContextType {
    isAuthenticated: boolean;
    userType: string | null;
    userEmail: string | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
    isAuthenticated: false,
    userType: null,
    userEmail: null,
    login: async () => {},
    logout: async () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userType, setUserType] = useState<string | null>(null);
    const [userEmail, setUserEmail] = useState<string | null>(null);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const isAuth = await authService.isAuthenticated();
            if (isAuth) {
                const userData = await authService.getCurrentUser();
                setIsAuthenticated(true);
                setUserType(userData.user_type);
                setUserEmail(userData.user_email);
            }
        } catch (error) {
            console.error('Error checking auth:', error);
        }
    };

    const login = async (email: string, password: string) => {
        try {
            const response = await authService.login({ username: email, password });
            setIsAuthenticated(true);
            setUserType(response.user_type);
            setUserEmail(response.user_email);
        } catch (error) {
            throw error;
        }
    };

    const logout = async () => {
        try {
            await authService.logout();
            setIsAuthenticated(false);
            setUserType(null);
        } catch (error) {
            console.error('Error logging out:', error);
        }
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, userType, userEmail, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
} 