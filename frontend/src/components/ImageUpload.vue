<template>
  <div
    class="min-h-screen flex items-start justify-center px-4 py-10 relative z-10"
  >
    <div class="w-full max-w-lg flex flex-col gap-5">
      <!-- Header -->
      <div class="flex flex-col gap-2">
        <span
          class="text-[.72rem] font-semibold tracking-widest uppercase text-[#cdff10] bg-[#cdff10]/10 px-3 py-1 rounded-full w-fit"
          >Paso 2 de 2</span
        >
        <h2 class="text-2xl font-bold text-white">Sube tus imágenes</h2>
        <p class="text-sm text-white/55">
          Hola, <strong class="text-[#05d16e]">{{ user.nombre }}</strong
          >{{ user.matricula ? ` (${user.matricula})` : "" }}. Puedes subir
          varias imágenes a la vez.
        </p>
      </div>

      <!-- Dropzone -->
      <div
        :class="[
          'border-2 border-dashed rounded-2xl text-center cursor-pointer transition-all duration-200',
          dragging
            ? 'border-[#05d16e] bg-[#05d16e]/[.07]'
            : 'border-[#05d16e]/35 bg-[#05d16e]/[.03] hover:border-[#05d16e] hover:bg-[#05d16e]/[.07]',
          queue.length ? 'py-4 px-4' : 'py-10 px-4',
        ]"
        @dragover.prevent="dragging = true"
        @dragleave="dragging = false"
        @drop.prevent="onDrop"
        @click="fileInput.click()"
      >
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          multiple
          class="hidden"
          @change="onFilePick"
        />
        <div v-if="!queue.length" class="flex flex-col items-center gap-3">
          <svg
            width="42"
            height="42"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#05d16e"
            stroke-width="1.5"
          >
            <rect x="3" y="3" width="18" height="18" rx="3" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <polyline points="21 15 16 10 5 21" />
          </svg>
          <p class="text-base font-semibold text-white/80">
            Arrastra imágenes aquí
          </p>
          <p class="text-xs text-white/40">
            o haz clic para seleccionar · máx. 5 MB por imagen
          </p>
        </div>
        <p
          v-else
          class="flex items-center justify-center gap-2 text-[#05d16e] text-sm font-semibold"
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
          >
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          Agregar más imágenes
        </p>
      </div>

      <!-- Queue -->
      <TransitionGroup
        name="list"
        tag="div"
        class="flex flex-col gap-2"
        v-if="queue.length"
      >
        <div
          v-for="item in queue"
          :key="item.id"
          :class="[
            'flex items-center gap-3 rounded-xl p-3 border transition-colors duration-200',
            item.status === 'done'
              ? 'bg-[#05d16e]/[.04] border-[#05d16e]/25'
              : item.status === 'error'
                ? 'bg-red-400/[.04] border-red-400/30'
                : item.status === 'loading'
                  ? 'bg-[#cdff10]/[.03] border-[#cdff10]/20'
                  : 'bg-white/[.04] border-white/[.08]',
          ]"
        >
          <!-- Thumb -->
          <div class="w-12 h-12 rounded-lg overflow-hidden flex-shrink-0">
            <img
              :src="item.preview"
              :alt="item.file.name"
              class="w-full h-full object-cover"
            />
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0 flex flex-col gap-1">
            <span class="text-[.82rem] font-semibold truncate text-white">{{
              item.file.name
            }}</span>
            <span
              :class="[
                'text-[.72rem]',
                item.sizeError ? 'text-red-400' : 'text-white/40',
              ]"
            >
              {{
                item.sizeError ? "⚠ Supera 5 MB" : formatSize(item.file.size)
              }}
            </span>
            <!-- Resultado -->
            <div
              v-if="item.status === 'done'"
              class="flex items-center gap-2 mt-0.5"
            >
              <span
                class="text-[.78rem] font-bold text-[#05d16e] bg-[#05d16e]/12 px-2 py-0.5 rounded-full"
                >{{ item.result.class }}</span
              >
              <span class="text-[.75rem] text-[#cdff10]"
                >{{ (item.result.confidence * 100).toFixed(1) }}%</span
              >
            </div>
            <div
              v-if="item.status === 'error'"
              class="text-[.75rem] text-red-400 mt-0.5"
            >
              {{ item.errorMsg }}
            </div>
            <!-- Progress -->
            <div
              v-if="item.status === 'loading'"
              class="w-full h-[3px] bg-white/10 rounded-full mt-1 overflow-hidden"
            >
              <div
                class="h-full w-2/5 bg-[#cdff10] rounded-full progress-anim"
              ></div>
            </div>
          </div>

          <!-- Remove / Check -->
          <button
            v-if="item.status === 'pending' || item.status === 'error'"
            class="text-white/35 p-1.5 rounded-full hover:text-red-400 hover:bg-red-400/10 transition-colors border-none bg-transparent cursor-pointer flex-shrink-0"
            @click.stop="remove(item.id)"
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
          <div v-if="item.status === 'done'" class="flex-shrink-0 p-1">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#05d16e"
              stroke-width="2.5"
            >
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
        </div>
      </TransitionGroup>

      <!-- Actions -->
      <div
        v-if="queue.length"
        class="flex items-center justify-between gap-4 flex-wrap"
      >
        <span class="text-xs text-white/45"
          >{{ pendingCount }} imagen{{ pendingCount !== 1 ? "es" : "" }} lista{{
            pendingCount !== 1 ? "s" : ""
          }}
          para enviar</span
        >
        <div class="flex gap-3 flex-wrap">
          <button
            @click="clearDone"
            class="flex items-center gap-2 py-2 px-5 rounded-lg bg-transparent text-[#05d16e] border border-[#05d16e] text-sm font-semibold cursor-pointer hover:bg-[#05d16e]/[.08] transition-colors"
          >
            Limpiar enviadas
          </button>
          <button
            @click="submitAll"
            :disabled="pendingCount === 0 || isUploading"
            :class="[
              'flex items-center gap-2 py-2 px-5 rounded-lg text-[#024653] font-semibold text-sm cursor-pointer border-none transition-all duration-200',
              pendingCount === 0 || isUploading
                ? 'bg-[#1a4a3a] text-[#3a6a5a] cursor-not-allowed'
                : 'bg-[#05d16e] hover:bg-[#08b662] hover:shadow-[0_0_0_4px_rgba(5,209,110,.2)] active:scale-[.97]',
            ]"
          >
            <svg
              v-if="!isUploading"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <polyline points="16 16 12 12 8 16" />
              <line x1="12" y1="12" x2="12" y2="21" />
              <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
            </svg>
            <span
              v-if="isUploading"
              class="w-4 h-4 border-2 border-[#024653]/40 border-t-[#024653] rounded-full animate-spin inline-block"
            ></span>
            {{ isUploading ? "Enviando..." : `Clasificar ${pendingCount}` }}
          </button>
        </div>
      </div>

      <!-- Restart -->
      <button
        @click="$emit('restart')"
        class="self-center flex items-center gap-2 py-2 px-5 rounded-lg bg-transparent text-[#05d16e] border border-[#05d16e] text-sm font-semibold cursor-pointer hover:bg-[#05d16e]/[.08] transition-colors mt-2"
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <polyline points="1 4 1 10 7 10" />
          <path d="M3.51 15a9 9 0 1 0 .49-4.95" />
        </svg>
        Empezar de nuevo
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({ user: Object });
defineEmits(["restart"]);

const fileInput = ref(null);
const queue = ref([]);
const dragging = ref(false);
const isUploading = ref(false);
let idCounter = 0;

const pendingCount = computed(
  () =>
    queue.value.filter((i) => i.status === "pending" && !i.sizeError).length,
);

function makeItem(file) {
  return {
    id: ++idCounter,
    file,
    preview: URL.createObjectURL(file),
    status: "pending",
    sizeError: file.size > 5 * 1024 * 1024,
    result: null,
    errorMsg: "",
  };
}
function addFiles(files) {
  for (const f of files) {
    if (f.type.startsWith("image/")) queue.value.push(makeItem(f));
  }
}
function onFilePick(e) {
  addFiles(e.target.files);
  e.target.value = "";
}
function onDrop(e) {
  dragging.value = false;
  addFiles(e.dataTransfer.files);
}
function remove(id) {
  queue.value = queue.value.filter((i) => i.id !== id);
}
function clearDone() {
  queue.value = queue.value.filter((i) => i.status !== "done");
}
function formatSize(b) {
  return b > 1024 * 1024
    ? (b / 1024 / 1024).toFixed(1) + " MB"
    : (b / 1024).toFixed(0) + " KB";
}

async function submitAll() {
  const pending = queue.value.filter(
    (i) => i.status === "pending" && !i.sizeError,
  );
  if (!pending.length) return;
  isUploading.value = true;
  for (const item of pending) {
    item.status = "loading";
    const fd = new FormData();
    fd.append("image", item.file);
    fd.append("nombre", props.user.nombre);
    if (props.user.matricula) fd.append("matricula", props.user.matricula);
    try {
      const res = await fetch("/api/classify/", { method: "POST", body: fd });
      const data = await res.json();
      if (!res.ok) {
        item.status = "error";
        item.errorMsg = Object.values(data).flat().join(" ");
      } else {
        item.status = "done";
        item.result = data;
      }
    } catch {
      item.status = "error";
      item.errorMsg = "Error de conexión.";
    }
  }
  isUploading.value = false;
}
</script>
