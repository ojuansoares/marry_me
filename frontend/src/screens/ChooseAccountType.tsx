// frontend/src/screens/ChooseAccountTypeScreen.tsx
import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const ChooseAccountTypeScreen = ({ navigation }: { navigation: any }) => {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>Escolha uma opção</Text>
            <Button
                title="Criar Conta"
                onPress={() => navigation.navigate('CreateAccount')}
            />
            <Button
                title="Login"
                onPress={() => navigation.navigate('Login')}
            />
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
});

export default ChooseAccountTypeScreen;