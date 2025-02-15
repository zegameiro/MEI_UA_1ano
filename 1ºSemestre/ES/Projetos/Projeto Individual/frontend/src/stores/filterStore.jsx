import { create } from "zustand";

export const useFilterSortStore = create((set) => ({
  filterOption: "",
  sortOption: "",
  sortOrder: "",

  setFilterOption: (option) => {
    set({ filterOption: option });
  },

  setSortOptions: (option, order) => {
    set({ sortOption: option, sortOrder: order });
  },
}));
