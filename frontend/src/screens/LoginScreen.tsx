import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import authService from '../services/authService';

export default function LoginScreen() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();

    const handleLogin = async () => {
        if (!email || !password) {
            Alert.alert('Erro', 'Por favor, preencha todos os campos');
            return;
        }

        try {
            setLoading(true);
            console.log('Iniciando login...');
            await login(email, password);
            console.log('Login realizado com sucesso');
        } catch (error) {
            console.error('Login error:', error);
            Alert.alert(
                'Erro de Login',
                error instanceof Error ? error.message : 'Erro ao fazer login. Verifique sua conexão com a internet.'
            );
        } finally {
            setLoading(false);
        }
    };

    const testConnection = async () => {
        try {
            setLoading(true);
            const isConnected = await authService.testConnection();
            Alert.alert(
                'Teste de Conexão',
                isConnected 
                    ? 'Conexão com o backend estabelecida com sucesso!'
                    : 'Não foi possível conectar ao backend. Verifique se o servidor está rodando.'
            );
        } catch (error) {
            console.error('Test connection error:', error);
            Alert.alert('Erro', 'Erro ao testar conexão');
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Login</Text>
            <TextInput
                style={styles.input}
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                editable={!loading}
            />
            <TextInput
                style={styles.input}
                placeholder="Senha"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
                editable={!loading}
            />
            <TouchableOpacity 
                style={[styles.button, loading && styles.buttonDisabled]} 
                onPress={handleLogin}
                disabled={loading}
            >
                <Text style={styles.buttonText}>
                    {loading ? 'Entrando...' : 'Entrar'}
                </Text>
            </TouchableOpacity>
            <TouchableOpacity 
                style={[styles.button, styles.testButton, loading && styles.buttonDisabled]} 
                onPress={testConnection}
                disabled={loading}
            >
                <Text style={styles.buttonText}>
                    Testar Conexão
                </Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        padding: 20,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        textAlign: 'center',
    },
    input: {
        borderWidth: 1,
        borderColor: '#ddd',
        padding: 10,
        borderRadius: 5,
        marginBottom: 10,
    },
    button: {
        backgroundColor: '#007AFF',
        padding: 15,
        borderRadius: 5,
        alignItems: 'center',
    },
    buttonDisabled: {
        backgroundColor: '#ccc',
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
    testButton: {
        backgroundColor: '#4CAF50',
        marginTop: 10,
    },
}); 