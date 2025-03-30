// frontend/src/screens/CreateAccountScreen.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { useAuth } from '../contexts/AuthContext';

const CreateAccountScreen = ({ navigation }: { navigation: any }) => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [userType, setUserType] = useState('guest'); // Default como convidado
    const { createUser } = useAuth();

    const handleCreateAccount = async () => {
        try {
            await createUser({ name, email, password, userType });
            Alert.alert('Sucesso', 'Conta criada com sucesso!');
            navigation.navigate('Login'); // Redireciona para a tela de login
        } catch (error: any) {
            Alert.alert('Erro', error.message);
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Criar Conta</Text>
            <TextInput
                placeholder="Nome"
                value={name}
                onChangeText={setName}
                style={styles.input}
            />
            <TextInput
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                style={styles.input}
                autoCapitalize="none"
            />
            <TextInput
                placeholder="Senha"
                value={password}
                onChangeText={setPassword}
                style={styles.input}
                secureTextEntry
            />
            <View style={styles.userTypeContainer}>
                <Button title="Noivo(a)" onPress={() => setUserType('fiance')} />
                <Button title="Convidado" onPress={() => setUserType('guest')} />
            </View>
            <Button title="Criar Conta" onPress={handleCreateAccount} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    title: {
        fontSize: 24,
        marginBottom: 20,
    },
    input: {
        width: '100%',
        padding: 10,
        borderWidth: 1,
        borderColor: '#ccc',
        marginBottom: 10,
        borderRadius: 5,
    },
    userTypeContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '100%',
        marginBottom: 10,
    },
});

export default CreateAccountScreen;