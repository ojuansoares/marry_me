import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';

interface AuthContextType {
    isAuthenticated: boolean;
    userType: string | null;
    login: (username: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [userType, setUserType] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        checkAuthStatus();
    }, []);

    const checkAuthStatus = async () => {
        try {
            const isAuth = await authService.isAuthenticated();
            if (isAuth) {
                const userData = await authService.getCurrentUser();
                setUserType(userData.user_type);
            }
            setIsAuthenticated(isAuth);
        } catch (error) {
            console.error('Error checking auth status:', error);
        } finally {
            setLoading(false);
        }
    };

    const login = async (username: string, password: string) => {
        try {
            const response = await authService.login({ username, password });
            setUserType(response.user_type);
            setIsAuthenticated(true);
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
        <AuthContext.Provider value={{ isAuthenticated, userType, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}; 