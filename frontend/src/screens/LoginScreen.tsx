import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import { useNavigation } from '@react-navigation/native';
import { NavigationProp } from '../types/navigation';

export default function LoginScreen() {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });
    const { login } = useAuth();
    const navigation = useNavigation<NavigationProp>();

    const handleChange = (name: string, value: string) => {
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async () => {
        if (!formData.username || !formData.password) {
            alert('Por favor, preencha todos os campos');
            return;
        }

        try {
            setLoading(true);
            await login(formData.username, formData.password);
            // A navegação será feita pelo ProtectedRoute
        } catch (error) {
            alert('Erro ao fazer login. Verifique suas credenciais.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={{ flex: 1, padding: 20, justifyContent: 'center' }}>
            <Text style={{ fontSize: 24, marginBottom: 20, textAlign: 'center' }}>Login</Text>
            
            <TextInput
                placeholder="Usuário"
                value={formData.username}
                onChangeText={(value) => handleChange('username', value)}
                style={{ borderWidth: 1, borderColor: '#ccc', padding: 10, marginBottom: 10 }}
            />
            
            <TextInput
                placeholder="Senha"
                value={formData.password}
                onChangeText={(value) => handleChange('password', value)}
                secureTextEntry
                style={{ borderWidth: 1, borderColor: '#ccc', padding: 10, marginBottom: 20 }}
            />
            
            <TouchableOpacity 
                onPress={handleSubmit}
                disabled={loading}
                style={{ backgroundColor: '#007AFF', padding: 15, borderRadius: 5 }}
            >
                {loading ? (
                    <ActivityIndicator color="white" />
                ) : (
                    <Text style={{ color: 'white', textAlign: 'center' }}>Entrar</Text>
                )}
            </TouchableOpacity>
        </View>
    );
} 