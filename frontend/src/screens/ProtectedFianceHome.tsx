import React from 'react';
import { View, Text } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import FianceHomeScreen from './FianceHomeScreen';
import Header from '../components/Header';
export default function ProtectedFianceHome() {
    const { isAuthenticated, userType } = useAuth();

    if (!isAuthenticated || userType !== 'fiance') {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text>Carregando...</Text>
            </View>
        );
    }

    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Header />
            <FianceHomeScreen />
        </View>
    );
} 