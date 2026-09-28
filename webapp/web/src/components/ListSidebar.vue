<script setup>
  import { ref } from 'vue';

  defineProps({
    lists: { type: Array, required: true },
    selected: { type: String, default: null },
  });
  const emit = defineEmits(['select', 'create', 'delete']);

  const newListName = ref('');

  function submitCreate() {
    const name = newListName.value.trim();
    if (!name) return;
    emit('create', name);
    newListName.value = '';
  }
</script>

<template>
  <aside class="sidebar">
    <h1>Pi-hole Lists</h1>

    <form class="new-list-form" @submit.prevent="submitCreate">
      <input v-model="newListName" placeholder="new-list-name" aria-label="New list name" />
      <button type="submit">+ New list</button>
    </form>

    <ul class="list-nav">
      <li v-for="list in lists" :key="list.name" :class="{ active: list.name === selected }">
        <button class="list-nav-item" @click="emit('select', list.name)">
          <span class="name">{{ list.name }}</span>
          <span class="count">{{ list.item_count.toLocaleString() }}</span>
        </button>
        <button class="delete-btn" title="Delete list" @click="emit('delete', list.name)">✕</button>
      </li>
      <li v-if="lists.length === 0" class="empty">No lists yet.</li>
    </ul>
  </aside>
</template>

<style scoped>
  .sidebar {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    width: 280px;
    min-width: 280px;
    border-right: 1px solid var(--border);
    height: 100vh;
    box-sizing: border-box;
    overflow-y: auto;
  }
  h1 {
    font-size: 1.1rem;
    margin: 0;
  }
  .new-list-form {
    display: flex;
    gap: 0.5rem;
  }
  .new-list-form input {
    flex: 1;
    min-width: 0;
  }
  .list-nav {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  .list-nav li {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
  .list-nav-item {
    flex: 1;
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
    text-align: left;
    background: transparent;
    border: none;
    padding: 0.5rem 0.6rem;
    border-radius: 6px;
    color: inherit;
    cursor: pointer;
  }
  .list-nav-item:hover {
    background: var(--bg-hover);
  }
  .active .list-nav-item {
    background: var(--accent);
    color: white;
  }
  .name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .count {
    opacity: 0.7;
    font-variant-numeric: tabular-nums;
  }
  .delete-btn {
    background: transparent;
    border: none;
    color: var(--danger);
    cursor: pointer;
    padding: 0.25rem 0.4rem;
    border-radius: 4px;
  }
  .delete-btn:hover {
    background: var(--bg-hover);
  }
  .empty {
    opacity: 0.6;
    padding: 0.5rem 0.6rem;
  }
</style>
