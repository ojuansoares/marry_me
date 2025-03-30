import React from 'react';
import { AuthProvider } from './src/contexts/AuthContext';
import LoginScreen from './src/screens/LoginScreen';
import ProtectedFianceHome from './src/screens/ProtectedFianceHome';
import ProtectedGuestHome from './src/screens/ProtectedGuestHome';
import { useAuth } from './src/contexts/AuthContext';
import { createStackNavigator } from '@react-navigation/stack';
import ChooseAccountTypeScreen from './src/screens/ChooseAccountType';
import CreateAccountScreen from './src/screens/CreateAccount';
import { NavigationContainer } from '@react-navigation/native';

const Stack = createStackNavigator();

function AppContent() {
    const { isAuthenticated, userType } = useAuth();

    if (!isAuthenticated) {
        return (
            <Stack.Navigator screenOptions={{ headerShown: false }}>
                <Stack.Screen name="ChooseAccount" component={ChooseAccountTypeScreen} />
                <Stack.Screen name="Login" component={LoginScreen} />
                <Stack.Screen name="CreateAccount" component={CreateAccountScreen} />
            </Stack.Navigator>
        );
    }

    if (userType === 'fiance') {
        return <ProtectedFianceHome />;
    }
    if (userType === 'guest') {
        return <ProtectedGuestHome />;
    }

    return <LoginScreen />;
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

