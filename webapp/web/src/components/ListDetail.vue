<script setup>
  import { ref, watch } from 'vue';
  import { addItem, getItems, removeItem } from '../api.js';

  const props = defineProps({
    listName: { type: String, required: true },
  });
  const emit = defineEmits(['changed']);

  const query = ref('');
  const page = ref(1);
  const pageSize = 50;
  const items = ref([]);
  const total = ref(0);
  const loading = ref(false);
  const error = ref('');
  const newDomain = ref('');

  let queryDebounce = null;

  async function load() {
    loading.value = true;
    error.value = '';
    try {
      const data = await getItems(props.listName, {
        query: query.value,
        page: page.value,
        pageSize,
      });
      items.value = data.items;
      total.value = data.total;
    } catch (e) {
      error.value = e.message;
    } finally {
      loading.value = false;
    }
  }

  watch(
    () => props.listName,
    () => {
      query.value = '';
      page.value = 1;
      load();
    },
    { immediate: true },
  );

  watch(query, () => {
    clearTimeout(queryDebounce);
    queryDebounce = setTimeout(() => {
      page.value = 1;
      load();
    }, 250);
  });

  watch(page, load);

  async function submitAdd() {
    const domain = newDomain.value.trim();
    if (!domain) return;
    error.value = '';
    try {
      await addItem(props.listName, domain);
      newDomain.value = '';
      await load();
      emit('changed');
    } catch (e) {
      error.value = e.message;
    }
  }

  async function handleRemove(domain) {
    error.value = '';
    try {
      await removeItem(props.listName, domain);
      await load();
      emit('changed');
    } catch (e) {
      error.value = e.message;
    }
  }

  function totalPages() {
    return Math.max(1, Math.ceil(total.value / pageSize));
  }
</script>

<template>
  <section class="detail">
    <header>
      <h2>{{ listName }}</h2>
      <span class="total">{{ total.toLocaleString() }} entries</span>
    </header>

    <div class="toolbar">
      <input v-model="query" placeholder="Search domain…" aria-label="Search domain" />
      <form class="add-form" @submit.prevent="submitAdd">
        <input v-model="newDomain" placeholder="add-domain.example" aria-label="New domain" />
        <button type="submit">Add</button>
      </form>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading" class="loading">Loading…</p>

    <ul v-else class="items">
      <li v-for="domain in items" :key="domain">
        <span>{{ domain }}</span>
        <button class="delete-btn" title="Remove" @click="handleRemove(domain)">✕</button>
      </li>
      <li v-if="items.length === 0" class="empty">No entries match.</li>
    </ul>

    <footer class="pager">
      <button :disabled="page <= 1" @click="page--">← Prev</button>
      <span>Page {{ page }} / {{ totalPages() }}</span>
      <button :disabled="page >= totalPages()" @click="page++">Next →</button>
    </footer>
  </section>
</template>

<style scoped>
  .detail {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
    height: 100vh;
    box-sizing: border-box;
  }
  header {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }
  h2 {
    margin: 0;
  }
  .total {
    opacity: 0.7;
  }
  .toolbar {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }
  .toolbar input {
    min-width: 220px;
  }
  .add-form {
    display: flex;
    gap: 0.5rem;
  }
  .error {
    color: var(--danger);
  }
  .items {
    list-style: none;
    margin: 0;
    padding: 0;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
  }
  .items li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--border);
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  }
  .items li:last-child {
    border-bottom: none;
  }
  .items li:nth-child(even) {
    background: var(--bg-alt);
  }
  .delete-btn {
    background: transparent;
    border: none;
    color: var(--danger);
    cursor: pointer;
  }
  .empty {
    opacity: 0.6;
    font-family: inherit;
  }
  .pager {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
  }
</style>
