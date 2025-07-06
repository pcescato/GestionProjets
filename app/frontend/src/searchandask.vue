<template>
  <div class="query-box">
    <h2>Interroger vos notes</h2>
    <form @submit.prevent="handleSearch">
      <input
        v-model="query"
        type="text"
        placeholder="Posez une question ou tapez un mot-clé..."
        required
      />
      <button :disabled="loading">{{ loading ? "Recherche..." : "Rechercher" }}</button>
    </form>

    <div v-if="results.length > 0">
      <h3>Résultats</h3>
      <ul>
        <li v-for="(r, i) in results" :key="i">
          {{ r.content.substring(0, 150) }}...
        </li>
      </ul>
    </div>

    <div v-if="answer">
      <h3>Réponse IA</h3>
      <p>{{ answer }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const query = ref("");
const loading = ref(false);
const results = ref([]);
const answer = ref("");

async function handleSearch() {
  loading.value = true;
  results.value = [];
  answer.value = "";

  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query.value)}`);
    const data = await res.json();
    results.value = data.results;
    answer.value = data.answer;
  } catch (e) {
    console.error(e);
    answer.value = "Erreur lors de la recherche.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.query-box {
  margin-top: 40px;
  padding: 10px;
  background: #f9f9f9;
}
input {
  width: 60%;
  padding: 8px;
}
button {
  margin-left: 10px;
  padding: 8px 16px;
}
</style>
