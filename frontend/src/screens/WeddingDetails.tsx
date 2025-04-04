import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { useWedding } from '../contexts/WeddingContext';
import { format } from 'date-fns';
import { pt } from 'date-fns/locale';

export default function WeddingDetailsScreen({ navigation }: { navigation: any }) {
  const { wedding, deleteWedding } = useWedding();

  if (!wedding) {
    return (
      <View style={styles.container}>
        <Text>Casamento não encontrado.</Text>
      </View>
    );
  }

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return format(date, "dd 'de' MMMM 'de' yyyy", { locale: pt });
    } catch (error) {
      return dateString;
    }
  };

  const handleDelete = () => {
    Alert.alert(
      "Confirmação",
      "Tem certeza que deseja excluir este casamento? Esta ação não pode ser desfeita.",
      [
        { text: "Cancelar", style: "cancel" },
        { 
          text: "Excluir", 
          style: "destructive",
          onPress: async () => {
            try {
              await deleteWedding();
              Alert.alert("Sucesso", "Casamento excluído com sucesso!");
              navigation.navigate('FianceHomeScreen');
            } catch (error) {
              Alert.alert("Erro", "Não foi possível excluir o casamento.");
            }
          }
        }
      ]
    );
  };

  const handleEdit = () => {
    // navigation.navigate('EditWedding', { wedding });
    return;
  };

  return (
    <ScrollView style={styles.scrollView}>
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>Detalhes do Casamento</Text>
          <Text style={styles.subtitle}>{formatDate(wedding.w_date)}</Text>
        </View>

        <View style={styles.card}>
          <View style={styles.infoRow}>
            <Text style={styles.label}>Data:</Text>
            <Text style={styles.value}>{formatDate(wedding.w_date)}</Text>
          </View>
          
          <View style={styles.infoRow}>
            <Text style={styles.label}>Local:</Text>
            <Text style={styles.value}>{wedding.w_location}</Text>
          </View>
          
          <View style={styles.infoRow}>
            <Text style={styles.label}>Status:</Text>
            <View style={[styles.statusBadge, 
              wedding.w_status === 'Planejamento' && styles.statusPlanning,
              wedding.w_status === 'Confirmado' && styles.statusConfirmed,
              wedding.w_status === 'Concluído' && styles.statusCompleted,
            ]}>
              <Text style={styles.statusText}>{wedding.w_status}</Text>
            </View>
          </View>
          
          <View style={styles.descriptionContainer}>
            <Text style={styles.label}>Descrição:</Text>
            <Text style={styles.description}>{wedding.w_description || "Nenhuma descrição fornecida."}</Text>
          </View>
        </View>

        <View style={styles.buttonsContainer}>
          <TouchableOpacity style={styles.editButton} onPress={handleEdit}>
            <Text style={styles.editButtonText}>Editar Casamento</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.deleteButton} onPress={handleDelete}>
            <Text style={styles.deleteButtonText}>Excluir Casamento</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollView: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  container: {
    flex: 1,
    padding: 20,
  },
  header: {
    marginBottom: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
    marginTop: 5,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    marginBottom: 20,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#555',
    width: 80,
  },
  value: {
    fontSize: 16,
    color: '#333',
    flex: 1,
  },
  descriptionContainer: {
    marginTop: 10,
  },
  description: {
    fontSize: 16,
    color: '#333',
    marginTop: 10,
    lineHeight: 22,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 20,
    backgroundColor: '#ccc',
  },
  statusPlanning: {
    backgroundColor: '#FFF9C4',
  },
  statusConfirmed: {
    backgroundColor: '#C8E6C9',
  },
  statusCompleted: {
    backgroundColor: '#BBDEFB',
  },
  statusText: {
    fontSize: 14,
    fontWeight: '500',
  },
  buttonsContainer: {
    marginTop: 20,
  },
  editButton: {
    backgroundColor: '#3498db',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 10,
  },
  editButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  deleteButton: {
    backgroundColor: '#e74c3c',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  deleteButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});