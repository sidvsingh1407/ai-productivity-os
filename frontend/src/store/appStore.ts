import { create } from 'zustand';

interface AppState {
  disclaimerAcknowledged: boolean;
  setDisclaimerAcknowledged: (value: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  disclaimerAcknowledged: localStorage.getItem('tarkhax_disclaimer') === 'true',
  setDisclaimerAcknowledged: (value) => {
    localStorage.setItem('tarkhax_disclaimer', String(value));
    set({ disclaimerAcknowledged: value });
  },
}));