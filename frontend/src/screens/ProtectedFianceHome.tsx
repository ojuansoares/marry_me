import React from 'react';
import { View, Text } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { useNavigation } from '@react-navigation/native';
import { NavigationProp } from '../types/navigation';
import FianceHomeScreen from './FianceHomeScreen';

export default function ProtectedFianceHome() {
    const { isAuthenticated, userType } = useAuth();
    const navigation = useNavigation<NavigationProp>();

    React.useEffect(() => {
        if (!isAuthenticated) {
            navigation.navigate('Login');
            return;
        }

        if (userType && userType !== 'fiance') {
            alert('Você não tem permissão para acessar esta tela.');
            navigation.navigate('Login');
        }
    }, [isAuthenticated, userType, navigation]);

    if (!isAuthenticated || (userType && userType !== 'fiance')) {
        return (
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text>Carregando...</Text>
            </View>
        );
    }

    return <FianceHomeScreen />;
} 