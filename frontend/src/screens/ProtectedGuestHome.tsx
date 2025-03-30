import React from 'react';
import { View, Text } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import GuestHomeScreen from './GuestHomeScreen';

export default function ProtectedGuestHome() {
    const { isAuthenticated, userType } = useAuth();

    if (!isAuthenticated || userType !== 'guest') {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text>Carregando...</Text>
            </View>
        );
    }

    return <GuestHomeScreen />;
} 