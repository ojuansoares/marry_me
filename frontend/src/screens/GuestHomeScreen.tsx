import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function GuestHomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bem-vindo Convidado!</Text>
      <Text style={styles.subtitle}>Área do Convidado</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
  },
}); 