import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  accessToken: localStorage.getItem('accessToken') || '',
  user: null,
  setSession: ({ accessToken, user }) => {
    localStorage.setItem('accessToken', accessToken);
    set({ accessToken, user });
  },
  logout: () => {
    localStorage.removeItem('accessToken');
    set({ accessToken: '', user: null });
  },
}));
