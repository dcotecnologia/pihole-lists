import js from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';
import eslintConfigPrettier from 'eslint-config-prettier';
import globals from 'globals';

export default [
  { ignores: ['dist/**', 'node_modules/**'] },
  js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: { ...globals.browser, ...globals.node },
    },
  },
  {
    rules: {
      'vue/multi-word-component-names': 'off',
    },
  },
  // Must stay last: turns off ESLint stylistic rules that would conflict
  // with Prettier, which owns formatting (see ../../.prettierrc).
  eslintConfigPrettier,
];
