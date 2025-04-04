import React from 'react';
import { View, Text } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import FianceHomeScreen from './FianceHomeScreen';
import Header from '../components/Header';
import { WeddingProvider } from '../contexts/WeddingContext';

export default function ProtectedFianceHome({ navigation }: { navigation: any }) {
    const { isAuthenticated, userType } = useAuth();

    if (!isAuthenticated || userType !== 'fiance') {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text>Carregando...</Text>
            </View>
        );
    }

    const navigateTo = (screen: string) => {
        navigation.navigate(screen);
    };

    return (
        <View style={{ flex: 1 }}>
            <Header />
            <WeddingProvider>
                <FianceHomeScreen navigation={{ navigate: navigateTo }} />
            </WeddingProvider>
        </View>
    );
}