<template>
  <div class="container">
    <h1>Nouvelle note</h1>
    <toast-ui-editor
      ref="editorRef"
      :initialValue="initialContent"
      :height="'400px'"
      usageStatistics="false"
      :previewStyle="'vertical'"
      :initialEditType="'wysiwyg'"
    />
    <button @click="handleSubmit" :disabled="loading" style="margin-top: 10px;">
      {{ loading ? "Enregistrement..." : "Enregistrer" }}
    </button>
    <p v-if="status" style="margin-top: 10px;">{{ status }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Editor from "@toast-ui/editor";
import "@toast-ui/editor/dist/toastui-editor.css";
import { Editor as ToastEditor } from "@toast-ui/vue3-editor";

const editorRef = ref(null);
const loading = ref(false);
const status = ref("");
const initialContent = "";

async function handleSubmit() {
  if (!editorRef.value) return;
  const markdown = editorRef.value.getInstance().getMarkdown();
  if (!markdown.trim()) {
    status.value = "Le contenu est vide.";
    return;
  }

  loading.value = true;
  status.value = "";

  try {
    const res = await fetch("/api/documents", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: markdown }),
    });
    if (!res.ok) throw new Error("Erreur API");
    const data = await res.json();
    status.value = `Enregistré avec ID ${data.id}, tags: ${data.tags.join(", ")}`;
    editorRef.value.getInstance().setMarkdown("");
  } catch (e) {
    status.value = "Erreur lors de l’enregistrement.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 30px auto;
  font-family: Arial, sans-serif;
}
button {
  padding: 8px 16px;
  font-size: 1rem;
}
</style>
