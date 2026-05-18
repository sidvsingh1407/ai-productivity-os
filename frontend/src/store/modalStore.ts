import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ModalState {
  hasAcknowledgedNotice: boolean
  isModalOpen: boolean
  pendingRoute: string | null

  // Actions
  setAcknowledged: (status: boolean) => void
  openModal: (route: string) => void
  closeModal: () => void
  clearPendingRoute: () => void
}

export const useModalStore = create<ModalState>()(
  persist(
    (set) => ({
      hasAcknowledgedNotice: false,
      isModalOpen: false,
      pendingRoute: null,

      setAcknowledged: (status) => set({ hasAcknowledgedNotice: status }),

      openModal: (route) => set({ isModalOpen: true, pendingRoute: route }),

      closeModal: () => set({ isModalOpen: false }),

      clearPendingRoute: () => set({ pendingRoute: null })
    }),
    {
      name: 'tarkhax-modal-storage',
      // Only persist the acknowledgment status
      partialize: (state) => ({ hasAcknowledgedNotice: state.hasAcknowledgedNotice }),
    }
  )
)
