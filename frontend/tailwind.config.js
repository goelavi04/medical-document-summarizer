/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
        mono: ["IBM Plex Mono", "Menlo", "monospace"],
      },
      colors: {
        // Restrained clinical palette: slate neutrals + a single muted teal accent.
        // Deliberately avoids purple/blue gradient "AI demo" aesthetics.
        ink: {
          950: "#0b1220",
          900: "#111827",
          800: "#1f2937",
          700: "#334155",
          600: "#475569",
          500: "#64748b",
          400: "#94a3b8",
          300: "#cbd5e1",
          200: "#e2e8f0",
          100: "#f1f5f9",
          50: "#f8fafc",
        },
        accent: {
          800: "#0f4c4c",
          700: "#14615f",
          600: "#187874",
          500: "#1d8f89",
          100: "#e3f2f1",
          50: "#f2f9f8",
        },
        caution: {
          700: "#92400e",
          500: "#d97706",
          100: "#fef3c7",
          50: "#fffbeb",
        },
        critical: {
          700: "#b91c1c",
          500: "#dc2626",
          100: "#fee2e2",
          50: "#fef2f2",
        },
      },
      boxShadow: {
        panel: "0 1px 2px rgba(15, 23, 42, 0.06), 0 1px 1px rgba(15, 23, 42, 0.04)",
      },
    },
  },
  plugins: [],
}
