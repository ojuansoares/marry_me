import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useWedding } from '../contexts/WeddingContext';

export default function FianceHomeScreen({ navigation }: { navigation: any }) {
  const { wedding, createWedding } = useWedding();

  const handleCreateWedding = () => {
    // Navegar para a tela de criação de casamento
    navigation.navigate('CreateWeddingScreen');
  };

  const handleViewWedding = () => {
    // Navegar para a tela de detalhes do casamento
    navigation.navigate('WeddingDetails', { weddingId: wedding.id });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bem-vindo Noivo!</Text>
      
      {!wedding ? (
        // Se não houver casamento, mostrar botão para criar
        <View style={styles.noWeddingContainer}>
          <Text style={styles.subtitle}>Você ainda não possui um casamento registrado.</Text>
          <TouchableOpacity 
            style={styles.createButton}
            onPress={handleCreateWedding}
          >
            <Text style={styles.buttonText}>Criar Casamento</Text>
          </TouchableOpacity>
        </View>
      ) : (
        // Se houver casamento, mostrar informações básicas e botão para ver detalhes
        <TouchableOpacity 
          style={styles.weddingCard}
          onPress={handleViewWedding}
        >
          <Text style={styles.weddingTitle}>Seu Casamento</Text>
          <Text style={styles.weddingDetail}>Data: {wedding.w_date}</Text>
          <Text style={styles.weddingDetail}>Local: {wedding.w_location}</Text>
          <Text style={styles.weddingDetail}>Status: {wedding.w_status}</Text>
          <Text style={styles.viewMoreText}>Toque para ver mais detalhes</Text>
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    width: '100%',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  noWeddingContainer: {
    alignItems: 'center',
    width: '100%',
  },
  createButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 12,
    paddingHorizontal: 30,
    borderRadius: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  weddingCard: {
    backgroundColor: '#f5f5f5',
    borderRadius: 10,
    padding: 20,
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    width: '100%',
  },
  weddingTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#444',
  },
  weddingDetail: {
    fontSize: 16,
    marginBottom: 8,
    color: '#555',
  },
  viewMoreText: {
    color: '#3498db',
    fontSize: 14,
    marginTop: 10,
    textAlign: 'center',
  },
});