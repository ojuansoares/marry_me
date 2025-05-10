import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { useWedding } from '../contexts/WeddingContext';
import { WeddingCreate, WeddingUpdate } from '../services/weddingService';
import DateTimePicker from '@react-native-community/datetimepicker';
import { format } from 'date-fns';

export default function CreateWeddingScreen({ navigation }: { navigation: any }) {  
  const { createWedding } = useWedding();
  const [date, setDate] = useState(new Date());
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [weddingData, setWeddingData] = useState<WeddingCreate>({
    w_date: format(new Date(), 'yyyy-MM-dd'),
    w_location: '',
    w_description: '',
    w_status: 'active',
  });

  const handleDateChange = (event: any, selectedDate: any) => {
    const currentDate = selectedDate || date;
    setShowDatePicker(false);
    setDate(currentDate);
    setWeddingData({
      ...weddingData,
      w_date: format(currentDate, 'yyyy-MM-dd'),
    });
  };

  const handleCreateWedding = async () => {
    try {
      if (!weddingData.w_location.trim()) {
        Alert.alert('Atenção', 'Por favor, informe o local do casamento.');
        return;
      }

      await createWedding(weddingData);
      console.log('Casamento:', weddingData);
      Alert.alert('Sucesso', 'Casamento criado com sucesso!');
      navigation.navigate('ProtectedFianceScreen');
    } catch (error) {
      console.error('Erro ao criar casamento:', error);
      Alert.alert('Erro', 'Não foi possível criar o casamento. Tente novamente.');
    }
  };

  const handleUpdateWedding = async () => {
    try {
        
    } catch (error) {
        console.error('Erro ao atualizar o casamento', error);
    }
  }
 
  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <View style={styles.container}>
        <Text style={styles.title}>Criar Novo Casamento</Text>
    
        <View style={styles.formGroup}>
          <Text style={styles.label}>Data do Casamento</Text>
          <TouchableOpacity 
            style={styles.dateInput}
            onPress={() => setShowDatePicker(true)}
          >
            <Text>{format(date, 'dd/MM/yyyy')}</Text>
          </TouchableOpacity>
          {showDatePicker && (
            <DateTimePicker
              value={date}
              mode="date"
              display="default"
              onChange={handleDateChange}
              minimumDate={new Date()}
            />
          )}
        </View>
    
        <View style={styles.formGroup}>
          <Text style={styles.label}>Local</Text>
          <TextInput
            style={styles.input}
            placeholder="Onde será realizado o casamento?"
            value={weddingData.w_location}
            onChangeText={(text) => setWeddingData({...weddingData, w_location: text})}
          />
        </View>
    
        <View style={styles.formGroup}>
          <Text style={styles.label}>Descrição</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="Descreva detalhes do seu casamento..."
            value={weddingData.w_description}
            onChangeText={(text) => setWeddingData({...weddingData, w_description: text})}
            multiline
            numberOfLines={4}
          />
        </View>
    
        <TouchableOpacity 
          style={styles.createButton}
          onPress={handleCreateWedding}
        >
          <Text style={styles.buttonText}>Criar Casamento</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.cancelButton}
          onPress={() => navigation.navigate('ProtectedFianceScreen')}
        >
          <Text style={styles.cancelButtonText}>Cancelar</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
  },
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
    textAlign: 'center',
  },
  formGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    marginBottom: 8,
    fontWeight: '500',
    color: '#333',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  textArea: {
    height: 100,
    textAlignVertical: 'top',
  },
  dateInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    backgroundColor: '#f9f9f9',
  },
  createButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  cancelButton: {
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  cancelButtonText: {
    color: '#666',
    fontSize: 16,
  },
});