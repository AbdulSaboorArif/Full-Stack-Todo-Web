import { createContext, useContext, useEffect, useState } from "react";
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id: number;
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
}

const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: true,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            throw new Error("Login failed");
          }

          const data = await response.json();
          setToken(data.access_token);

          // Fetch user info
          const userResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/user`, {
            headers: {
              "Authorization": `Bearer ${data.access_token}`,
            },
          });

          if (userResponse.ok) {
            const userData = await userResponse.json();
            setUser({
              id: userData.id,
              email: userData.email,
            });
          }
        } catch (error) {
          throw error;
        }
      },

      register: async (email: string, password: string) => {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            throw new Error("Registration failed");
          }

          const data = await response.json();
          setToken(data.access_token);

          // Fetch user info
          const userResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/user`, {
            headers: {
              "Authorization": `Bearer ${data.access_token}`,
            },
          });

          if (userResponse.ok) {
            const userData = await response.json();
            setUser({
              id: userData.id,
              email: userData.email,
            });
          }
        } catch (error) {
          throw error;
        }
      },

      logout: () => {
        setToken(null);
        setUser(null);
      },

      setUser: (user: User | null) => {
        set({ user, isAuthenticated: !!user });
      },

      setToken: (token: string | null) => {
        if (token) {
          localStorage.setItem("token", token);
          set({ token, isAuthenticated: true });
        } else {
          localStorage.removeItem("token");
          set({ token: null, isAuthenticated: false });
        }
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      useAuthStore.setState({
        token,
        isAuthenticated: true,
      });

      // Verify token
      const verifyToken = async () => {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/user`, {
            headers: {
              "Authorization": `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const userData = await response.json();
            useAuthStore.setState({
              user: {
                id: userData.id,
                email: userData.email,
              },
              isLoading: false,
            });
          } else {
            useAuthStore.setState({
              token: null,
              user: null,
              isAuthenticated: false,
              isLoading: false,
            });
          }
        } catch (error) {
          useAuthStore.setState({
            token: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      };

      verifyToken();
    } else {
      useAuthStore.setState({
        isLoading: false,
      });
    }

    setInitialized(true);
  }, []);

  if (!initialized) {
    return <div>Loading...</div>;
  }

  return <>{children}</>;
};

export const useAuth = () => {
  return useAuthStore((state) => ({
    user: state.user,
    token: state.token,
    isLoading: state.isLoading,
    isAuthenticated: state.isAuthenticated,
    login: state.login,
    register: state.register,
    logout: state.logout,
  }));
};

export const AuthContext = createContext<AuthState | undefined>(undefined);