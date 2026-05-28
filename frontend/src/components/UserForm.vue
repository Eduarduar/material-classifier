<template>
  <div
    class="min-h-screen flex flex-col md:items-center md:justify-center md:px-4 md:py-12 relative z-10"
  >
    <div class="flex flex-col flex-1 md:hidden">
      <div
        class="sticky top-0 z-10 bg-[#024653]/95 backdrop-blur-md border-b border-white/[.06] px-5 py-4 flex items-center gap-4"
      >
        <button
          @click="$emit('back')"
          class="w-9 h-9 rounded-xl bg-white/[.06] border border-white/10 flex items-center justify-center text-white/60 cursor-pointer border-none flex-shrink-0 active:scale-90 transition-transform"
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
          >
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-1">
            <!-- Progress bar -->
            <div class="flex-1 h-1 bg-white/10 rounded-full overflow-hidden">
              <div class="h-full w-1/2 bg-[#05d16e] rounded-full"></div>
            </div>
            <span class="text-[.65rem] text-white/40 font-medium">1/2</span>
          </div>
          <p class="text-xs text-white/50">Cuéntanos sobre ti</p>
        </div>
      </div>

      <!-- Contenido scrolleable -->
      <div class="flex-1 overflow-y-auto px-5 py-6 flex flex-col gap-5">
        <div>
          <h2 class="text-2xl font-bold text-white mb-1">Tu información</h2>
          <p class="text-sm text-white/45">
            Necesitamos algunos datos para registrar tu aportación.
          </p>
        </div>

        <div class="flex flex-col gap-2">
          <label
            class="text-xs font-semibold text-[#05d16e] uppercase tracking-wider"
            >Nombre completo</label
          >
          <input
            v-model="form.nombre"
            type="text"
            placeholder="Ej. María García López"
            :class="[
              'bg-white/[.06] border rounded-xl text-white text-base px-4 py-3.5 outline-none transition-all placeholder:text-white/25',
              errors.nombre
                ? 'border-red-400'
                : 'border-white/10 focus:border-[#05d16e]',
            ]"
            @input="errors.nombre = ''"
          />
          <span v-if="errors.nombre" class="text-xs text-red-400">{{
            errors.nombre
          }}</span>
        </div>

        <div
          @click="form.esEstudiante = !form.esEstudiante"
          :class="[
            'flex items-center gap-4 p-4 rounded-xl border cursor-pointer transition-all active:scale-[.98]',
            form.esEstudiante
              ? 'bg-[#05d16e]/10 border-[#05d16e]/40'
              : 'bg-white/[.04] border-white/10',
          ]"
        >
          <span
            :class="[
              'w-6 h-6 rounded-lg border-2 flex items-center justify-center flex-shrink-0 transition-all',
              form.esEstudiante
                ? 'bg-[#05d16e] border-[#05d16e]'
                : 'border-white/25',
            ]"
          >
            <svg
              v-if="form.esEstudiante"
              width="12"
              height="12"
              viewBox="0 0 12 12"
              fill="none"
            >
              <path
                d="M2 6l3 3 5-5"
                stroke="#024653"
                stroke-width="2.2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </span>
          <div>
            <p class="text-sm font-semibold text-white">
              Soy estudiante de la UdeC
            </p>
            <p class="text-xs text-white/40 mt-0.5">Universidad de Colima</p>
          </div>
        </div>

        <Transition name="slide">
          <div v-if="form.esEstudiante" class="flex flex-col gap-2">
            <label
              class="text-xs font-semibold text-[#05d16e] uppercase tracking-wider"
              >Número de matrícula</label
            >
            <input
              v-model="form.matricula"
              type="tel"
              placeholder="Entre 8 y 10 dígitos"
              maxlength="10"
              :class="[
                'bg-white/[.06] border rounded-xl text-white text-base px-4 py-3.5 outline-none transition-all placeholder:text-white/25',
                errors.matricula
                  ? 'border-red-400'
                  : 'border-white/10 focus:border-[#05d16e]',
              ]"
              @input="onMatriculaInput"
            />
            <span v-if="errors.matricula" class="text-xs text-red-400">{{
              errors.matricula
            }}</span>
          </div>
        </Transition>

        <div
          @click="form.aceptaTerminos = !form.aceptaTerminos"
          :class="[
            'flex items-start gap-4 p-4 rounded-xl border cursor-pointer transition-all active:scale-[.98]',
            form.aceptaTerminos
              ? 'bg-[#05d16e]/10 border-[#05d16e]/40'
              : 'bg-white/[.04] border-white/10',
          ]"
        >
          <span
            :class="[
              'w-6 h-6 rounded-lg border-2 flex items-center justify-center flex-shrink-0 mt-0.5 transition-all',
              form.aceptaTerminos
                ? 'bg-[#05d16e] border-[#05d16e]'
                : 'border-white/25',
            ]"
          >
            <svg
              v-if="form.aceptaTerminos"
              width="12"
              height="12"
              viewBox="0 0 12 12"
              fill="none"
            >
              <path
                d="M2 6l3 3 5-5"
                stroke="#024653"
                stroke-width="2.2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </span>
          <div class="flex-1">
            <p class="text-sm text-white/80 leading-relaxed">
              Acepto los
              <span
                class="text-[#05d16e] underline"
                @click.stop="showTerms = true"
                >términos y condiciones</span
              >
              y el
              <span
                class="text-[#05d16e] underline"
                @click.stop="showTerms = true"
                >aviso de privacidad</span
              >
            </p>
          </div>
        </div>
        <span v-if="errors.terminos" class="text-xs text-red-400 -mt-3">{{
          errors.terminos
        }}</span>
      </div>

      <div
        class="px-5 pb-8 pt-4 border-t border-white/[.06] bg-[#024653]/95 backdrop-blur-md"
      >
        <button
          @click="submit"
          class="w-full flex items-center justify-center gap-3 py-4 rounded-2xl bg-[#05d16e] text-[#024653] font-bold text-base cursor-pointer border-none active:scale-[.97] transition-transform"
        >
          Continuar
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

    <div class="hidden md:flex w-full max-w-md flex-col gap-5">
      <button
        @click="$emit('back')"
        class="flex items-center gap-2 bg-transparent border-none text-white/50 text-sm cursor-pointer hover:text-[#05d16e] transition-colors w-fit p-0"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
        Volver
      </button>
      <div class="flex flex-col gap-2">
        <span
          class="text-[.72rem] font-semibold tracking-widest uppercase text-[#cdff10] bg-[#cdff10]/10 px-3 py-1 rounded-full w-fit"
          >Paso 1 de 2</span
        >
        <h2 class="text-2xl font-bold text-white">Cuéntanos sobre ti</h2>
        <p class="text-sm text-white/50">
          Esta información nos ayuda a reconocer tu contribución al dataset.
        </p>
      </div>
      <div
        class="bg-white/[.04] border border-white/[.09] rounded-2xl backdrop-blur-xl p-8"
      >
        <div class="flex flex-col gap-1.5 mb-5">
          <label
            class="text-[.82rem] font-semibold text-[#05d16e] uppercase tracking-wider"
            >Nombre completo</label
          >
          <input
            v-model="form.nombre"
            type="text"
            placeholder="Ej. María García López"
            :class="[
              'bg-white/[.06] border rounded-lg text-white text-[.95rem] px-4 py-3 outline-none transition-all placeholder:text-white/30',
              errors.nombre
                ? 'border-red-400'
                : 'border-white/10 focus:border-[#05d16e] focus:bg-[#05d16e]/[.06]',
            ]"
            @input="errors.nombre = ''"
          />
          <span v-if="errors.nombre" class="text-xs text-red-400">{{
            errors.nombre
          }}</span>
        </div>
        <label class="flex items-center gap-3 mb-5 cursor-pointer select-none">
          <input type="checkbox" v-model="form.esEstudiante" class="hidden" />
          <span
            :class="[
              'w-5 h-5 border-2 rounded-md flex items-center justify-center flex-shrink-0 transition-all',
              form.esEstudiante
                ? 'bg-[#05d16e] border-[#05d16e]'
                : 'border-white/25 hover:border-[#05d16e]',
            ]"
          >
            <svg
              v-if="form.esEstudiante"
              width="10"
              height="10"
              viewBox="0 0 12 12"
              fill="none"
            >
              <path
                d="M2 6l3 3 5-5"
                stroke="#024653"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </span>
          <span class="text-sm text-white/80"
            >Soy estudiante de la Universidad de Colima</span
          >
        </label>
        <Transition name="slide">
          <div v-if="form.esEstudiante" class="flex flex-col gap-1.5 mb-5">
            <label
              class="text-[.82rem] font-semibold text-[#05d16e] uppercase tracking-wider"
              >Número de matrícula</label
            >
            <input
              v-model="form.matricula"
              type="text"
              placeholder="Número de matrícula"
              maxlength="10"
              :class="[
                'bg-white/[.06] border rounded-lg text-white text-[.95rem] px-4 py-3 outline-none transition-all placeholder:text-white/30',
                errors.matricula
                  ? 'border-red-400'
                  : 'border-white/10 focus:border-[#05d16e] focus:bg-[#05d16e]/[.06]',
              ]"
              @input="onMatriculaInput"
            />
            <span v-if="errors.matricula" class="text-xs text-red-400">{{
              errors.matricula
            }}</span>
          </div>
        </Transition>
        <div class="mb-6">
          <label class="flex items-center gap-3 cursor-pointer select-none">
            <input
              type="checkbox"
              v-model="form.aceptaTerminos"
              class="hidden"
            />
            <span
              :class="[
                'w-5 h-5 border-2 rounded-md flex items-center justify-center flex-shrink-0 transition-all',
                form.aceptaTerminos
                  ? 'bg-[#05d16e] border-[#05d16e]'
                  : 'border-white/25 hover:border-[#05d16e]',
              ]"
            >
              <svg
                v-if="form.aceptaTerminos"
                width="10"
                height="10"
                viewBox="0 0 12 12"
                fill="none"
              >
                <path
                  d="M2 6l3 3 5-5"
                  stroke="#024653"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </span>
            <span class="text-sm text-white/80">
              Acepto los
              <a
                href="#"
                class="text-[#05d16e] underline underline-offset-2"
                @click.prevent="showTerms = true"
                >términos y condiciones</a
              >
              y el
              <a
                href="#"
                class="text-[#05d16e] underline underline-offset-2"
                @click.prevent="showTerms = true"
                >aviso de privacidad</a
              >
            </span>
          </label>
          <span
            v-if="errors.terminos"
            class="text-xs text-red-400 mt-1 block"
            >{{ errors.terminos }}</span
          >
        </div>
        <button
          @click="submit"
          class="w-full flex items-center justify-center gap-2 py-3 px-8 rounded-lg bg-[#05d16e] text-[#024653] font-semibold text-[.95rem] cursor-pointer border-none transition-all hover:bg-[#08b662] hover:shadow-[0_0_0_4px_rgba(5,209,110,.2)] active:scale-[.97]"
        >
          Continuar
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

    <Transition name="fade">
      <div
        v-if="showTerms"
        class="fixed inset-0 z-50 bg-[#02161c]/90 backdrop-blur-md flex items-end md:items-center justify-center md:p-6"
        @click.self="showTerms = false"
      >
        <div
          class="w-full md:max-w-md bg-[#032d38] border border-white/[.09] rounded-t-3xl md:rounded-2xl p-6 md:p-8 flex flex-col gap-5"
        >
          <div
            class="w-10 h-1 bg-white/20 rounded-full mx-auto md:hidden"
          ></div>
          <h3 class="text-lg font-bold text-white">
            Términos y Condiciones / Aviso de Privacidad
          </h3>
          <div class="flex flex-col gap-3 max-h-64 overflow-y-auto pr-1">
            <p class="text-sm text-white/65 leading-relaxed">
              Las imágenes que subas serán utilizadas exclusivamente para
              mejorar el modelo de clasificación de materiales reciclables del
              proyecto RENOVA.
            </p>
            <p class="text-sm text-white/65 leading-relaxed">
              Tu nombre y matrícula (en caso de proporcionarla) se usarán
              únicamente para el reconocimiento de tu contribución al proyecto.
            </p>
            <p class="text-sm text-white/65 leading-relaxed">
              No compartiremos tu información personal con terceros. Las
              imágenes pasan a formar parte del dataset de entrenamiento de
              acceso interno, aunque en el futuro este dataset podría llegar a
              ser de acceso público para investigación.
            </p>
            <p class="text-sm text-white/65 leading-relaxed">
              Puedes solicitar la eliminación de tus datos en cualquier momento
              contactando al equipo RENOVA al correo:
              <a
                href="mailto:soyrenovaapp@gmail.com"
                class="text-[#05d16e] underline"
                >soyrenovaapp@gmail.com</a
              >
            </p>
          </div>
          <button
            @click="acceptTerms"
            class="w-full py-3.5 rounded-xl bg-[#05d16e] text-[#024653] font-bold cursor-pointer border-none hover:bg-[#08b662] transition-colors active:scale-[.97]"
          >
            Aceptar y cerrar
          </button>
        </div>
      </div>
    </Transition>

    <Transition name="fade">
      <div
        v-if="showWarning"
        class="fixed inset-0 z-50 bg-[#02161c]/90 backdrop-blur-md flex items-end md:items-center justify-center md:p-6"
      >
        <div
          class="w-full md:max-w-md bg-[#032d38] border border-[#cdff10]/20 rounded-t-3xl md:rounded-2xl p-6 md:p-8 flex flex-col gap-5"
        >
          <div
            class="w-10 h-1 bg-white/20 rounded-full mx-auto md:hidden"
          ></div>
          <div class="flex justify-center">
            <div
              class="w-14 h-14 rounded-2xl bg-[#cdff10]/10 flex items-center justify-center"
            >
              <svg
                width="28"
                height="28"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#cdff10"
                stroke-width="2"
              >
                <path
                  d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                />
                <line x1="12" y1="9" x2="12" y2="13" />
                <line x1="12" y1="17" x2="12.01" y2="17" />
              </svg>
            </div>
          </div>
          <h3 class="text-lg font-bold text-white text-center">
            Antes de subir imágenes
          </h3>
          <div class="flex flex-col gap-3">
            <div
              v-for="tip in tips"
              :key="tip.text"
              class="flex items-start gap-3 p-3 bg-white/[.03] rounded-xl"
            >
              <span class="text-lg">{{ tip.icon }}</span>
              <p
                class="text-sm text-white/70 leading-relaxed"
                v-html="tip.text"
              ></p>
            </div>
          </div>
          <button
            @click="confirm"
            class="w-full py-3.5 rounded-xl bg-[#05d16e] text-[#024653] font-bold cursor-pointer border-none hover:bg-[#08b662] transition-colors active:scale-[.97]"
          >
            Entendido, continuar
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";

const emit = defineEmits(["next", "back"]);

const tips = [
  {
    icon: "📏",
    text: 'Cada imagen no debe superar <strong class="text-[#cdff10]">8 MB</strong>',
  },
  { icon: "💡", text: "Sube imágenes claras y bien iluminadas" },
  { icon: "🎯", text: "El material debe ser el objeto principal de la foto" },
  { icon: "🔒", text: "No subas imágenes con información personal visible" },
];

const form = reactive({
  nombre: "",
  esEstudiante: false,
  matricula: "",
  aceptaTerminos: false,
});
const errors = reactive({ nombre: "", matricula: "", terminos: "" });
const showTerms = ref(false);
const showWarning = ref(false);

function onMatriculaInput() {
  form.matricula = form.matricula.replace(/\D/g, "").slice(0, 10);
  errors.matricula = "";
}
function acceptTerms() {
  form.aceptaTerminos = true;
  showTerms.value = false;
}
function validate() {
  let ok = true;
  errors.nombre = errors.matricula = errors.terminos = "";
  if (!form.nombre.trim()) {
    errors.nombre = "El nombre es requerido.";
    ok = false;
  }
  if (form.esEstudiante && form.matricula && form.matricula.length < 8) {
    errors.matricula = "Mínimo 8 dígitos.";
    ok = false;
  }
  if (!form.aceptaTerminos) {
    errors.terminos = "Debes aceptar los términos y condiciones.";
    ok = false;
  }
  return ok;
}
function submit() {
  if (validate()) showWarning.value = true;
}
function confirm() {
  showWarning.value = false;
  emit("next", {
    nombre: form.nombre.trim(),
    matricula: form.esEstudiante ? form.matricula : "",
  });
}
</script>
