import React from 'react';
import { View, Text } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { useNavigation } from '@react-navigation/native';
import { NavigationProp } from '../types/navigation';
import GuestHomeScreen from './GuestHomeScreen';

export default function ProtectedGuestHome() {
    const { isAuthenticated, userType } = useAuth();
    const navigation = useNavigation<NavigationProp>();

    React.useEffect(() => {
        if (!isAuthenticated) {
            navigation.navigate('Login');
            return;
        }

        if (userType && userType !== 'guest') {
            alert('Você não tem permissão para acessar esta tela.');
            navigation.navigate('Login');
        }
    }, [isAuthenticated, userType, navigation]);

    if (!isAuthenticated || (userType && userType !== 'guest')) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text>Carregando...</Text>
            </View>
        );
    }

    return <GuestHomeScreen />;
} 