/**
 * Jest setup file for the mobile app
 */

import '@testing-library/jest-native/extend-expect';

// Mock react-native-config
jest.mock('react-native-config', () => ({
  API_URL: 'http://localhost:3001',
  JWT_SECRET: 'test-jwt-secret',
  ABACUS_API_KEY: 'test-abacus-api-key',
  GOOGLE_CLOUD_API_KEY: 'test-google-cloud-api-key',
}));

// Mock react-native-dotenv
jest.mock('react-native-dotenv', () => ({
  API_URL: 'http://localhost:3001',
  JWT_SECRET: 'test-jwt-secret',
  ABACUS_API_KEY: 'test-abacus-api-key',
  GOOGLE_CLOUD_API_KEY: 'test-google-cloud-api-key',
}));

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () => ({
  setItem: jest.fn(() => Promise.resolve()),
  getItem: jest.fn(() => Promise.resolve(null)),
  removeItem: jest.fn(() => Promise.resolve()),
  clear: jest.fn(() => Promise.resolve()),
}));

// Mock react-native-gesture-handler
jest.mock('react-native-gesture-handler', () => {
  const View = require('react-native').View;
  return {
    Swipeable: View,
    DrawerLayout: View,
    State: {},
    ScrollView: View,
    Slider: View,
    Switch: View,
    TextInput: View,
    ToolbarAndroid: View,
    ViewPagerAndroid: View,
    DrawerLayoutAndroid: View,
    WebView: View,
    NativeViewGestureHandler: View,
    TapGestureHandler: View,
    FlingGestureHandler: View,
    ForceTouchGestureHandler: View,
    LongPressGestureHandler: View,
    PanGestureHandler: View,
    PinchGestureHandler: View,
    RotationGestureHandler: View,
    /* Buttons */
    RawButton: View,
    BaseButton: View,
    RectButton: View,
    BorderlessButton: View,
    /* Other */
    FlatList: View,
    gestureHandlerRootHOC: jest.fn(),
    Directions: {},
  };
});

// Mock react-native-reanimated
jest.mock('react-native-reanimated', () => {
  const Reanimated = require('react-native-reanimated/mock');
  Reanimated.default.call = () => {};
  return Reanimated;
});

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
    ok: true,
    status: 200,
    statusText: 'OK',
  })
);
