import React from 'react';
import { AuthProvider } from './src/contexts/AuthContext';
import LoginScreen from './src/screens/LoginScreen';
import ProtectedFianceHome from './src/screens/ProtectedFianceHome';
import ProtectedGuestHome from './src/screens/ProtectedGuestHome';
import { useAuth } from './src/contexts/AuthContext';
import ChooseAccountTypeScreen from './src/screens/ChooseAccountType';
import CreateAccountScreen from './src/screens/CreateAccount';
import { NavigationContainer } from '@react-navigation/native';
import WeddingDetails from './src/screens/WeddingDetails';
import CreateWeddingScreen from './src/screens/CreateWeddingScreen';

function AppContent() {
    const { isAuthenticated, userType } = useAuth();
    const [currentScreen, setCurrentScreen] = React.useState('ChooseAccountType');

    const navigateTo = (screen: string) => {
        setCurrentScreen(screen);
    };

    if (!isAuthenticated) {
        if (currentScreen === 'ChooseAccountType') {
            return (
                <ChooseAccountTypeScreen navigation={{ navigate: navigateTo }} />
            );
        }
        if (currentScreen === 'Login') {
            return (
                <LoginScreen navigation={{ navigate: navigateTo }} />
            );
        }
        if (currentScreen === 'CreateAccount') {
            return (
                <CreateAccountScreen navigation={{ navigate: navigateTo }} />
            );
        }
    }

    if (currentScreen === 'FianceHomeScreen') {
        return <ProtectedFianceHome navigation={{ navigate: navigateTo }} />;
    }
    if (currentScreen === 'WeddingDetails') {
        return <WeddingDetails navigation={{ navigate: navigateTo }} />;
    }
    if (currentScreen === 'CreateWeddingScreen') {
        return <CreateWeddingScreen navigation={{ navigate: navigateTo }} />;
    }
    if (userType === 'fiance') {
        return <ProtectedFianceHome navigation={{navigate: navigateTo}} />;
    }
    if (userType === 'guest') {
        return <ProtectedGuestHome navigation={{navigate: navigateTo}} />;
    }

    return <LoginScreen navigation={{navigate: navigateTo}} />; 
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

