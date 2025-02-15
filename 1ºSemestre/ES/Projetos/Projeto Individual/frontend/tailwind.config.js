
const { nextui } = require("@nextui-org/react");

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#7d46a4",
        secondary: "#cb9fc5",
        accent: "#bb819f",
        error: "#ef5b71",
        success: "#55b480",
        text: "#0f1a47",
        background: "#faf9fb",
      },
    },
  },
  darkMode: "class",
  plugins: [nextui({})],
}

