// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}", // Проверьте эту строку!
  ],
  theme: {
    extend: {
      colors: {
        frstrmaincolor: '#151515',
        secondmaincolor: '#252525',
      }
    },
  },
  plugins: [],
}