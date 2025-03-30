// frontend/src/components/Header.tsx
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet, Alert, Modal } from 'react-native';
import { useAuth } from '../contexts/AuthContext';

const Header = () => {
    const { userType, userEmail, logout } = useAuth();
    const [modalVisible, setModalVisible] = useState(false);

    const handleLogout = async () => {
        await logout();
        Alert.alert('Logout', 'Você foi desconectado.');
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Marry Me</Text>
            <TouchableOpacity onPress={() => setModalVisible(true)}>
                <Image
                    source={{ uri: 'https://cdn-icons-png.freepik.com/512/9706/9706583.png' }} // URL da imagem genérica
                    style={styles.profileImage}
                />
            </TouchableOpacity>
            <Modal
                animationType="fade"
                transparent={true}
                visible={modalVisible}
                onRequestClose={() => setModalVisible(false)}
            >
                <View style={styles.modalContainer}>
                    <View style={styles.modalContent}>
                        <Text style={styles.username}>{userEmail}</Text>
                        <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
                            <Text style={styles.logoutText}>Logout</Text>
                        </TouchableOpacity>
                        <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeButton}>
                            <Text style={styles.closeText}>Fechar</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        justifyContent: 'space-between', // Isso garante que os elementos fiquem nas extremidades
        alignItems: 'center',
        padding: 10,
        backgroundColor: '#f8f8f8',
        borderBottomWidth: 1,
        borderBottomColor: '#ddd',
        paddingTop: 40, // Para evitar que fique atrás da barra do celular
    },
    title: {
        fontSize: 20,
        fontWeight: 'bold',
        flex: 1, // Isso faz com que o título ocupe o espaço disponível à esquerda
    },
    profileImage: {
        width: 40,
        height: 40,
        borderRadius: 20,
    },
    modalContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(0, 0, 0, 0.5)', // Fundo semi-transparente
    },
    modalContent: {
        width: 300,
        padding: 20,
        backgroundColor: 'white',
        borderRadius: 10,
        alignItems: 'center',
    },
    username: {
        fontSize: 18,
        marginBottom: 20,
    },
    logoutButton: {
        backgroundColor: '#ff4d4d',
        padding: 10,
        borderRadius: 5,
        marginBottom: 10,
    },
    logoutText: {
        color: 'white',
        fontWeight: 'bold',
    },
    closeButton: {
        backgroundColor: '#ccc',
        padding: 10,
        borderRadius: 5,
    },
    closeText: {
        color: 'black',
    },
});

export default Header;