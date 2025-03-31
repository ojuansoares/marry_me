// frontend/src/screens/CreateAccountScreen.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert, Animated, TouchableOpacity } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import Collapsible from 'react-native-collapsible';

const CreateAccountScreen = ({ navigation }: { navigation: any }) => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [phone, setPhone] = useState('');
    const [userType, setUserType] = useState('');
    const [userTypeDisplay, setUserTypeDisplay] = useState('');
    const { createUser } = useAuth();
    const [isCollapsed, setIsCollapsed] = useState(true);

    const toggleAccordion = () => {
        setIsCollapsed(!isCollapsed);
    };

    const handleCreateAccount = async () => {
        try {
            await createUser({ u_name: name, u_email: email, u_phone: phone, u_password: password, u_type: userType });
            Alert.alert('Sucesso', 'Conta criada com sucesso!');
            navigation.navigate('Login');
        } catch (error: any) {
            Alert.alert('Erro', error.message);
        }
    };

    const handleUserTypeSelect = (type: string, displayName: string) => {
        setUserType(type);
        setUserTypeDisplay(displayName);
        toggleAccordion();
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
                placeholder="Telefone"
                value={phone}
                onChangeText={setPhone}
                style={styles.input}
            />
            <TextInput
                placeholder="Senha"
                value={password}
                onChangeText={setPassword}
                style={styles.input}
                secureTextEntry
            />
             <TouchableOpacity onPress={toggleAccordion} style={styles.selection}>
                <Text style={styles.selectionText}>
                    {userTypeDisplay || 'Selecione o Tipo de Usuário'}
                </Text>
            </TouchableOpacity>
            <Collapsible collapsed={isCollapsed}>
                <View style={styles.optionsContainer}>
                    <TouchableOpacity
                        style={styles.option}
                        onPress={() => handleUserTypeSelect('fiance', 'Noivo(a)')}
                    >
                        <Text style={styles.optionText}>Noivo(a)</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        style={styles.option}
                        onPress={() => handleUserTypeSelect('guest', 'Convidado')}
                    >
                        <Text style={styles.optionText}>Convidado</Text>
                    </TouchableOpacity>
                </View>
            </Collapsible>
            <View style={styles.buttonContainer}>
                <TouchableOpacity style={styles.backButton} onPress={() => navigation.navigate('ChooseAccountType')}>
                    <Text style={styles.backButtonText}>Voltar</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.createButton} onPress={handleCreateAccount}>
                    <Text style={styles.createButtonText}>Criar Conta</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        fontSize: 24,
        marginBottom: 20,
    },
    input: {
        borderWidth: 1,
        borderColor: '#ddd',
        padding: 10,
        borderRadius: 5,
        marginBottom: 10,
        width: '80%',
    },
    selection: {
        padding: 10,
        backgroundColor: '#ddd',
        borderRadius: 5,
        width: '80%',
        alignItems: 'center',
    },
    selectionText: {
        fontSize: 18,
    },
    optionsContainer: {
        width: '100%',
        backgroundColor: '#ddd',
    },
    option: {
        backgroundColor: '#e0e0e0',
        padding: 10,
        borderRadius: 5,
        marginTop: 5,
        width: '100%',
        alignItems: 'center',
    },
    optionText: {
        fontSize: 16,
    },
    button: {
        backgroundColor: '#007AFF',
        padding: 15,
        borderRadius: 5,
        alignItems: 'center',
        marginTop: 20,
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
    backButton: {
        backgroundColor: '#007AFF',
        padding: 15,
        borderRadius: 5,
        alignItems: 'center',
        marginTop: 20,
    },
    createButton: {
        backgroundColor: '#007AFF',
        padding: 15,
        borderRadius: 5,
        alignItems: 'center',
        marginTop: 20,
    },
    backButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
    createButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
    buttonContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '80%',
    },
    backButtonContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '80%',
    },
});

export default CreateAccountScreen;