module.exports = {
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  overrides: [
    {
      files: ['src/tk22/core/**/*.{ts,tsx}'],
      rules: {
        'no-restricted-imports': [
          'error',
          {
            patterns: [
              '../adapters/*',
              '../../adapters/*',
              '../services/*',
              '../../services/*',
              '../agent/*',
              '../../agent/*',
              '../apis/*',
              '../../apis/*',
              '../gen/*',
              '../../gen/*',
              '../utils/*',
              '../../utils/*',
            ],
          },
        ],
      },
    },
  ],
}
