import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "media",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "rgb(var(--color-primary))", //main color
          shade: "rgb(var(--color-primary-shade))", //slightly darker main eg: hover
        },
        secondary: {
          DEFAULT: "rgb(var(--color-secondary))", //secondary color
          shade: "rgb(var(--color-secondary-shade))",
        },

        contrast: "rgb(var(--color-contrast))", //black or white text color
        canvas: "rgb(var(--color-canvas))", //background
        accent: "rgb(var(--color-accent))", //accent background

        brand: {
          gray: "#777777", //colors independent of dark/light mode, TUM gray
          white: "#ffffff", //eg: text inside buttons, TUM white
          darkblue: "#072140",
          darkbluehover: "#0d3a73",
          tumblue: "#3070b3",
          tumbluelight: "#4889ce",
          tumdark: "#333333",
          red: "#EF4444",
          green: "#a0af00", // TUM green
          darkgreen: "#515700",
          orange: "#e37222", // TUM orange
          orangehover: "#c7611c",
          smoke: "#E5E7EB", //eg: borders
          linkhover: "#c2d7ef",
          tablecolor: "#e6e6e6",
          tableborder: "#dadada",
        },
      },
      fontSize: {
        "title-lg": "2rem", //  main title size
        "title-md": "1.5rem", //  section title size
        body: "1rem", // body text size
      },
      borderRadius: {
        card: "0.5rem", //  border radius for card-like elements
      },
      boxShadow: {
        card: "0 2px 4px rgba(0, 0, 0, 0.1)", // Soft shadow for cards and UI elements
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
  },

  plugins: [],
};
export default config;
