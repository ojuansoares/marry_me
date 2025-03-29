import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { AuthProvider } from './src/contexts/AuthContext';
import LoginScreen from './src/screens/LoginScreen';
import ProtectedFianceHome from './src/screens/ProtectedFianceHome';
import ProtectedGuestHome from './src/screens/ProtectedGuestHome';
import { RootStackParamList } from './src/types/navigation';

const Stack = createNativeStackNavigator<RootStackParamList>();

function AppContent() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="Login" 
        component={LoginScreen}
        options={{ headerShown: false }}
      />
      <Stack.Screen 
        name="FianceHome" 
        component={ProtectedFianceHome}
        options={{ headerShown: false }}
      />
      <Stack.Screen 
        name="GuestHome" 
        component={ProtectedGuestHome}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <NavigationContainer>
        <AppContent />
      </NavigationContainer>
    </AuthProvider>
  );
}

