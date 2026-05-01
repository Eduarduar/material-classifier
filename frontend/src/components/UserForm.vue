<template>
  <div
    class="min-h-screen flex items-center justify-center px-4 py-12 relative z-10"
  >
    <div class="w-full max-w-md flex flex-col gap-5">
      <!-- Back -->
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

      <!-- Header -->
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

      <!-- Card -->
      <div
        class="bg-white/[.04] border border-white/[.09] rounded-2xl backdrop-blur-xl p-8"
      >
        <!-- Nombre -->
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
              'bg-white/[.06] border rounded-lg text-white font-[Poppins] text-[.95rem] px-4 py-3 outline-none transition-all duration-200 placeholder:text-white/30',
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

        <!-- Checkbox estudiante -->
        <label class="flex items-center gap-3 mb-5 cursor-pointer select-none">
          <input type="checkbox" v-model="form.esEstudiante" class="hidden" />
          <span
            :class="[
              'w-5 h-5 border-2 rounded-md flex items-center justify-center flex-shrink-0 transition-all duration-200',
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

        <!-- Matrícula -->
        <Transition name="slide">
          <div v-if="form.esEstudiante" class="flex flex-col gap-1.5 mb-5">
            <label
              class="text-[.82rem] font-semibold text-[#05d16e] uppercase tracking-wider"
              >Número de matrícula</label
            >
            <input
              v-model="form.matricula"
              type="text"
              placeholder="Numero de matrícula (opcional)"
              maxlength="10"
              :class="[
                'bg-white/[.06] border rounded-lg text-white font-[Poppins] text-[.95rem] px-4 py-3 outline-none transition-all duration-200 placeholder:text-white/30',
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

        <!-- Términos -->
        <div class="mb-6">
          <label class="flex items-center gap-3 cursor-pointer select-none">
            <input
              type="checkbox"
              v-model="form.aceptaTerminos"
              class="hidden"
            />
            <span
              :class="[
                'w-5 h-5 border-2 rounded-md flex items-center justify-center flex-shrink-0 transition-all duration-200',
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
                class="text-[#05d16e] underline underline-offset-2 hover:text-[#08b662]"
                @click.prevent="showTerms = true"
                >términos y condiciones</a
              >
              y el
              <a
                href="#"
                class="text-[#05d16e] underline underline-offset-2 hover:text-[#08b662]"
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
          class="w-full flex items-center justify-center gap-2 py-3 px-8 rounded-lg bg-[#05d16e] text-[#024653] font-semibold text-[.95rem] cursor-pointer border-none transition-all duration-200 hover:bg-[#08b662] hover:shadow-[0_0_0_4px_rgba(5,209,110,.2)] active:scale-[.97]"
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

    <!-- Modal términos -->
    <Transition name="fade">
      <div
        v-if="showTerms"
        class="fixed inset-0 z-50 bg-[#02161c]/85 backdrop-blur-md flex items-center justify-center p-6"
        @click.self="showTerms = false"
      >
        <div
          class="w-full max-w-md bg-white/[.04] border border-white/[.09] rounded-2xl backdrop-blur-xl p-8 flex flex-col gap-5"
        >
          <h3 class="text-lg font-bold text-white">
            Términos y Condiciones / Aviso de Privacidad
          </h3>
          <div class="flex flex-col gap-3 max-h-60 overflow-y-auto pr-2">
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
              contactando al equipo RENOVA, al correo:
              <a
                href="mailto:soyrenovaapp@gmail.com"
                class="text-[#05d16e] underline"
                >soyrenovaapp@gmail.com</a
              >
            </p>
          </div>
          <button
            @click="acceptTerms"
            class="w-full py-3 px-8 rounded-lg bg-[#05d16e] text-[#024653] font-semibold cursor-pointer border-none hover:bg-[#08b662] transition-colors"
          >
            Aceptar y cerrar
          </button>
        </div>
      </div>
    </Transition>

    <!-- Modal advertencia -->
    <Transition name="fade">
      <div
        v-if="showWarning"
        class="fixed inset-0 z-50 bg-[#02161c]/85 backdrop-blur-md flex items-center justify-center p-6"
      >
        <div
          class="w-full max-w-md bg-white/[.04] border border-[#cdff10]/25 rounded-2xl backdrop-blur-xl p-8 flex flex-col gap-5"
        >
          <div class="flex justify-center">
            <svg
              width="40"
              height="40"
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
          <h3 class="text-lg font-bold text-white text-center">
            Antes de subir imágenes
          </h3>
          <ul class="flex flex-col gap-2 pl-5 list-disc">
            <li class="text-sm text-white/70 leading-relaxed">
              Cada imagen no debe superar
              <strong class="text-[#cdff10]">5 MB</strong>
            </li>
            <li class="text-sm text-white/70 leading-relaxed">
              Sube imágenes claras y bien iluminadas
            </li>
            <li class="text-sm text-white/70 leading-relaxed">
              Asegúrate de que el material sea el objeto principal de la foto
            </li>
            <li class="text-sm text-white/70 leading-relaxed">
              No subas imágenes con información personal visible
            </li>
          </ul>
          <button
            @click="confirm"
            class="w-full py-3 px-8 rounded-lg bg-[#05d16e] text-[#024653] font-semibold cursor-pointer border-none hover:bg-[#08b662] transition-colors"
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
  if (form.esEstudiante) {
    if (!form.matricula) {
      errors.matricula = "Ingresa tu matrícula.";
      ok = false;
    } else if (form.matricula.length < 8) {
      errors.matricula = "Mínimo 8 dígitos.";
      ok = false;
    }
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
