import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

export const useUserStore = create(
  persist(
    (set, _get) => ({
      user_name: "",
      picture_url: "",
      isLoggedIn: false,
      credential: "",

      login: (user_name, picture_url, credential) => {
        set({
          user_name: user_name,
          picture_url: picture_url,
          isLoggedIn: true,
          credential: credential,
        });
      },

      logout: () => {
        set({
          first_name: "",
          last_name: "",
          picture_url: "",
          isLoggedIn: false,
          credential: "",
        });
      },
    }),
    {
      name: "user-store",
      storage: createJSONStorage(() => localStorage),
    }
  )
);
