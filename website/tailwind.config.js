/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        tux: {
          black: '#0d0d0d',
          darker: '#080808',
          dark: '#111111',
          card: '#161616',
          border: '#1e1e1e',
          orange: '#FF6A00',
          'orange-light': '#FF8C33',
          'orange-dim': '#FF6A00',
          blue: '#0EA5E9',
          'blue-light': '#38BDF8',
          'blue-dim': '#0284C7',
          text: '#E8E8E8',
          muted: '#888888',
          subtle: '#555555',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'stripe': 'stripe 4s linear infinite',
        'glow-orange': 'glowOrange 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        stripe: {
          '0%': { backgroundPosition: '0 0' },
          '100%': { backgroundPosition: '40px 40px' },
        },
        glowOrange: {
          '0%': { boxShadow: '0 0 20px rgba(255, 106, 0, 0.15)' },
          '100%': { boxShadow: '0 0 40px rgba(255, 106, 0, 0.3)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
      },
    },
  },
  plugins: [],
};
