import { NativeStackNavigationProp } from '@react-navigation/native-stack';

export type RootStackParamList = {
  Login: undefined;
  FianceHome: undefined;
  GuestHome: undefined;
};

export type NavigationProp = NativeStackNavigationProp<RootStackParamList>; 