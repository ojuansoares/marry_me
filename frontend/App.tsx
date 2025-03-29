import React from 'react';
import { AuthProvider } from './src/contexts/AuthContext';
import LoginScreen from './src/screens/LoginScreen';
import ProtectedFianceHome from './src/screens/ProtectedFianceHome';
import ProtectedGuestHome from './src/screens/ProtectedGuestHome';
import { useAuth } from './src/contexts/AuthContext';

function AppContent() {
    const { isAuthenticated, userType } = useAuth();

    if (!isAuthenticated) {
        return <LoginScreen />;
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
            <AppContent />
        </AuthProvider>
    );
}

