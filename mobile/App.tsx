import React, { useState } from 'react';
import {
  SafeAreaView,
  StatusBar,
  StyleSheet,
  Text,
  useColorScheme,
  View,
  Button,
} from 'react-native';
import Config from 'react-native-config';
import LoginScreen from './src/screens/LoginScreen';

const App = () => {
  const isDarkMode = useColorScheme() === 'dark';
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  const backgroundStyle = {
    backgroundColor: isDarkMode ? '#222' : '#F3F3F3',
    flex: 1,
  };

  const handleLogin = (token: string) => {
    setToken(token);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setToken(null);
    setIsLoggedIn(false);
  };

  return (
    <SafeAreaView style={backgroundStyle}>
      <StatusBar
        barStyle={isDarkMode ? 'light-content' : 'dark-content'}
        backgroundColor={backgroundStyle.backgroundColor}
      />
      
      {isLoggedIn ? (
        <View style={styles.container}>
          <Text style={styles.title}>Nick the Great Mobile</Text>
          <Text style={styles.subtitle}>You are logged in!</Text>
          
          <View style={styles.infoContainer}>
            <Text style={styles.infoTitle}>Environment Configuration</Text>
            <Text style={styles.infoText}>API URL: {Config.API_URL}</Text>
            
            {Config.GOOGLE_CLOUD_API_KEY ? (
              <Text style={styles.apiInfo}>Google Cloud API Key is configured</Text>
            ) : (
              <Text style={styles.apiWarning}>Google Cloud API Key is not set</Text>
            )}
            
            {Config.ABACUS_API_KEY ? (
              <Text style={styles.apiInfo}>Abacus API Key is configured</Text>
            ) : (
              <Text style={styles.apiWarning}>Abacus API Key is not set</Text>
            )}
          </View>
          
          <Button title="Logout" onPress={handleLogout} />
        </View>
      ) : (
        <LoginScreen onLogin={handleLogin} />
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 18,
    marginBottom: 24,
    color: '#666',
  },
  infoContainer: {
    width: '100%',
    backgroundColor: '#f5f5f5',
    padding: 16,
    borderRadius: 8,
    marginBottom: 24,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    marginBottom: 8,
  },
  apiInfo: {
    fontSize: 14,
    color: 'green',
    marginVertical: 4,
  },
  apiWarning: {
    fontSize: 14,
    color: 'orange',
    marginVertical: 4,
  },
});

export default App;
