<script setup>
  import { ref, onMounted } from 'vue';
  import ListSidebar from './components/ListSidebar.vue';
  import ListDetail from './components/ListDetail.vue';
  import { createList, deleteList, getLists } from './api.js';

  const lists = ref([]);
  const selected = ref(null);
  const error = ref('');

  async function refresh() {
    error.value = '';
    try {
      lists.value = await getLists();
      if (selected.value && !lists.value.some(l => l.name === selected.value)) {
        selected.value = null;
      }
    } catch (e) {
      error.value = e.message;
    }
  }

  async function handleCreate(name) {
    error.value = '';
    try {
      await createList(name);
      await refresh();
      selected.value = name;
    } catch (e) {
      error.value = e.message;
    }
  }

  async function handleDelete(name) {
    if (!confirm(`Delete list "${name}"? This cannot be undone.`)) return;
    error.value = '';
    try {
      await deleteList(name);
      await refresh();
    } catch (e) {
      error.value = e.message;
    }
  }

  onMounted(refresh);
</script>

<template>
  <div class="layout">
    <ListSidebar
      :lists="lists"
      :selected="selected"
      @select="n => (selected = n)"
      @create="handleCreate"
      @delete="handleDelete"
    />
    <main>
      <p v-if="error" class="error">{{ error }}</p>
      <ListDetail v-if="selected" :list-name="selected" @changed="refresh" />
      <p v-else class="placeholder">Select a list on the left, or create a new one.</p>
    </main>
  </div>
</template>

<style scoped>
  .layout {
    display: flex;
  }
  main {
    flex: 1;
    min-width: 0;
  }
  .error {
    color: var(--danger);
    padding: 1rem 1.5rem 0;
  }
  .placeholder {
    padding: 1.5rem;
    opacity: 0.7;
  }
</style>
