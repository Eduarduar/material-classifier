<template>
  <div
    class="min-h-screen flex flex-col md:items-center md:justify-center md:px-4 md:py-12 relative z-10"
  >
    <!-- ═══════════════════════════════════════════
         MODAL DE CORRECCIÓN — fuera de cualquier contenedor
         usando Teleport para evitar problemas de z-index y stacking
    ═══════════════════════════════════════════ -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="showCorrectionModal"
          class="fixed inset-0 z-[9999] bg-[#02161c]/90 backdrop-blur-md flex items-end md:items-center justify-center md:p-6"
          @click.self="closeCorrectionModal"
        >
          <div
            class="w-full md:max-w-sm bg-[#032d38] border border-white/[.09] rounded-t-3xl md:rounded-2xl p-6 md:p-8 flex flex-col gap-5"
          >
            <!-- Handle táctil móvil -->
            <div
              class="w-10 h-1 bg-white/20 rounded-full mx-auto md:hidden"
            ></div>

            <div class="flex flex-col gap-1">
              <h3 class="text-lg font-bold text-white">
                Corregir clasificación
              </h3>
              <p class="text-sm text-white/55">
                El modelo predijo
                <span class="text-[#cdff10] font-semibold">
                  {{ translateClass(itemToCorrect?.result?.class) }}
                </span>
                — selecciona la clase correcta.
              </p>
            </div>

            <!-- Select de clases -->
            <div class="flex flex-col gap-2">
              <label
                class="text-xs font-semibold text-[#05d16e] uppercase tracking-wider"
              >
                Clase correcta
              </label>
              <select
                v-model="selectedClass"
                class="bg-white/[.06] border border-white/10 rounded-lg text-white text-sm px-4 py-3 outline-none focus:border-[#05d16e] focus:bg-[#05d16e]/[.06] transition-colors"
              >
                <option value="" disabled>Selecciona una clase…</option>
                <option
                  v-for="cls in availableClasses"
                  :key="cls.value"
                  :value="cls.value"
                >
                  {{ cls.label }}
                </option>
              </select>
            </div>

            <!-- Estado de error en la corrección -->
            <p v-if="correctionError" class="text-sm text-red-400">
              {{ correctionError }}
            </p>

            <!-- Botones -->
            <div class="flex gap-3 flex-col-reverse md:flex-row">
              <button
                @click="closeCorrectionModal"
                :disabled="isCorrecting"
                class="flex-1 py-3 px-4 rounded-lg bg-white/[.06] border border-white/10 text-white font-semibold cursor-pointer hover:bg-white/[.08] transition-colors active:scale-[.97] disabled:opacity-50"
              >
                Cancelar
              </button>
              <button
                @click="submitCorrection"
                :disabled="!selectedClass || isCorrecting"
                class="flex-1 py-3 px-4 rounded-lg font-semibold cursor-pointer transition-all active:scale-[.97] flex items-center justify-center gap-2"
                :class="[
                  selectedClass && !isCorrecting
                    ? 'bg-[#05d16e] text-[#024653] hover:bg-[#08b662]'
                    : 'bg-white/10 text-white/30 cursor-not-allowed',
                ]"
              >
                <span
                  v-if="isCorrecting"
                  class="w-4 h-4 border-2 border-[#024653]/40 border-t-[#024653] rounded-full animate-spin"
                ></span>
                {{ isCorrecting ? "Guardando…" : "Guardar corrección" }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ═══════════════════════════════════════════
         MOBILE LAYOUT
    ═══════════════════════════════════════════ -->
    <div class="flex flex-col flex-1 md:hidden">
      <!-- Header fijo móvil -->
      <div
        class="sticky top-0 z-10 bg-[#024653]/95 backdrop-blur-md border-b border-white/[.06] px-5 py-4 flex items-center gap-4"
      >
        <button
          @click="$emit('restart')"
          class="w-9 h-9 rounded-xl bg-white/[.06] border border-white/10 flex items-center justify-center text-white/60 cursor-pointer flex-shrink-0 active:scale-90 transition-transform"
          style="border: none"
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
            <div class="flex-1 h-1 bg-white/10 rounded-full overflow-hidden">
              <div class="h-full w-full bg-[#05d16e] rounded-full"></div>
            </div>
            <span class="text-[.65rem] text-white/40 font-medium">2/2</span>
          </div>
          <p class="text-xs text-white/50">
            Hola,
            <span class="text-[#05d16e] font-semibold">{{ user.nombre }}</span>
          </p>
        </div>
      </div>

      <!-- Contenido scrolleable -->
      <div class="flex-1 overflow-y-auto flex flex-col">
        <!-- Zona de captura / selección -->
        <div class="px-5 pt-6 pb-4">
          <h2 class="text-2xl font-bold text-white mb-1">Sube tus imágenes</h2>
          <p class="text-sm text-white/45 mb-5">
            Toma una foto o selecciona desde tu galería.
          </p>

          <!-- Botones de acción primarios (móvil) -->
          <div class="flex gap-3 mb-5">
            <!-- Cámara -->
            <button
              v-if="hasCamera"
              @click="openCamera"
              class="flex-1 flex flex-col items-center justify-center gap-2 py-5 rounded-2xl bg-[#05d16e]/10 border border-[#05d16e]/30 active:scale-[.97] transition-transform cursor-pointer"
              style="border-width: 1px"
            >
              <svg
                width="28"
                height="28"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#05d16e"
                stroke-width="1.8"
              >
                <path
                  d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"
                />
                <circle cx="12" cy="13" r="4" />
              </svg>
              <span class="text-sm font-semibold text-[#05d16e]"
                >Tomar foto</span
              >
            </button>

            <!-- Galería -->
            <button
              @click="fileInput.click()"
              :class="[
                'flex-col items-center justify-center gap-2 py-5 rounded-2xl active:scale-[.97] transition-transform cursor-pointer',
                hasCamera ? 'flex-1 flex' : 'w-full flex',
                'bg-white/[.06] border border-white/15',
              ]"
              style="border-width: 1px; display: flex"
            >
              <svg
                width="28"
                height="28"
                viewBox="0 0 24 24"
                fill="none"
                stroke="rgba(255,255,255,0.7)"
                stroke-width="1.8"
              >
                <rect x="3" y="3" width="18" height="18" rx="3" />
                <circle cx="8.5" cy="8.5" r="1.5" />
                <polyline points="21 15 16 10 5 21" />
              </svg>
              <span class="text-sm font-semibold text-white/70">Galería</span>
            </button>
          </div>

          <!-- Inputs ocultos -->
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            multiple
            class="hidden"
            @change="onFilePick"
          />
          <input
            ref="cameraInput"
            type="file"
            accept="image/*"
            capture="environment"
            class="hidden"
            @change="onFilePick"
          />
        </div>

        <!-- Drop zone extra cuando ya hay items -->
        <div v-if="queue.length" class="mx-5 mb-4">
          <button
            @click="fileInput.click()"
            class="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-dashed border-[#05d16e]/30 text-[#05d16e] text-sm font-semibold active:scale-[.98] transition-transform cursor-pointer bg-transparent"
            style="border-style: dashed"
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
          </button>
        </div>

        <!-- Queue móvil -->
        <div class="px-5 flex flex-col gap-3 pb-4">
          <TransitionGroup name="list" tag="div" class="flex flex-col gap-3">
            <div
              v-for="item in queue"
              :key="item.id"
              :class="[
                'rounded-2xl border overflow-hidden transition-colors duration-200',
                item.status === 'done'
                  ? 'border-[#05d16e]/30 bg-[#05d16e]/[.05]'
                  : item.status === 'error'
                    ? 'border-red-400/30 bg-red-400/[.04]'
                    : item.status === 'loading'
                      ? 'border-[#cdff10]/20 bg-[#cdff10]/[.03]'
                      : 'border-white/10 bg-white/[.04]',
              ]"
            >
              <!-- Thumb -->
              <div class="relative w-full aspect-video bg-black/20">
                <img
                  :src="item.preview"
                  :alt="item.file.name"
                  class="w-full h-full object-cover"
                />
                <!-- Overlay loading -->
                <div
                  v-if="item.status === 'loading'"
                  class="absolute inset-0 bg-black/50 flex items-center justify-center"
                >
                  <div
                    class="w-8 h-8 border-2 border-[#cdff10]/30 border-t-[#cdff10] rounded-full animate-spin"
                  ></div>
                </div>
                <!-- Badge done -->
                <div
                  v-if="item.status === 'done'"
                  class="absolute top-3 right-3 w-8 h-8 bg-[#05d16e] rounded-full flex items-center justify-center shadow-lg"
                >
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="#024653"
                    stroke-width="3"
                  >
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
                <!-- Badge error -->
                <div
                  v-if="item.status === 'error'"
                  class="absolute top-3 right-3 w-8 h-8 bg-red-400 rounded-full flex items-center justify-center shadow-lg"
                >
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="white"
                    stroke-width="3"
                  >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </div>
                <!-- Botón eliminar -->
                <button
                  v-if="item.status === 'pending' || item.status === 'error'"
                  class="absolute top-3 left-3 w-8 h-8 bg-black/50 backdrop-blur-sm rounded-full flex items-center justify-center text-white/70 cursor-pointer active:scale-90 transition-transform"
                  style="border: none"
                  @click.stop="remove(item.id)"
                >
                  <svg
                    width="12"
                    height="12"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                  >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>

              <!-- Info -->
              <div class="px-4 py-3 flex flex-col gap-1">
                <div class="flex items-center justify-between gap-2">
                  <span class="text-sm font-semibold truncate text-white">{{
                    item.file.name
                  }}</span>
                  <span
                    :class="[
                      'text-xs flex-shrink-0',
                      item.sizeError ? 'text-red-400' : 'text-white/40',
                    ]"
                    >{{
                      item.sizeError ? "⚠ +8 MB" : formatSize(item.file.size)
                    }}</span
                  >
                </div>

                <!-- Resultado clasificación -->
                <div
                  v-if="item.status === 'done'"
                  class="flex flex-col gap-2 mt-1"
                >
                  <div class="flex items-center gap-2 flex-wrap">
                    <span
                      class="text-sm font-bold text-[#05d16e] bg-[#05d16e]/12 px-3 py-1 rounded-full"
                    >
                      {{ translateClass(item.result.class) }}
                    </span>
                    <span class="text-sm text-[#cdff10] font-semibold">
                      {{ (item.result.confidence * 100).toFixed(1) }}%
                    </span>
                    <!-- Badge "corregida" si ya fue corregida -->
                    <span
                      v-if="item.corrected"
                      class="text-xs text-white/40 bg-white/[.06] px-2 py-0.5 rounded-full"
                    >
                      ✓ Corregida
                    </span>
                  </div>
                  <button
                    @click="openCorrectionModal(item)"
                    class="text-xs text-white/60 font-semibold py-1.5 px-3 rounded-lg bg-white/[.06] border border-white/10 active:scale-95 transition-transform cursor-pointer flex items-center justify-center gap-1.5"
                    style="border-width: 1px"
                  >
                    <svg
                      width="11"
                      height="11"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2.5"
                    >
                      <path
                        d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                      />
                      <path
                        d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                      />
                    </svg>
                    Corregir clasificación
                  </button>
                </div>

                <!-- Error -->
                <p
                  v-if="item.status === 'error'"
                  class="text-sm text-red-400 mt-0.5"
                >
                  {{ item.errorMsg }}
                </p>

                <!-- Progress bar -->
                <div
                  v-if="item.status === 'loading'"
                  class="w-full h-[3px] bg-white/10 rounded-full mt-2 overflow-hidden"
                >
                  <div
                    class="h-full w-2/5 bg-[#cdff10] rounded-full progress-anim"
                  ></div>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>
      </div>
      <!-- /scrolleable -->

      <!-- CTA fijo abajo (móvil) -->
      <div
        v-if="queue.length"
        class="px-5 pb-8 pt-4 border-t border-white/[.06] bg-[#024653]/95 backdrop-blur-md flex flex-col gap-3"
      >
        <div class="flex items-center justify-between text-xs text-white/40">
          <span
            >{{ pendingCount }} lista{{ pendingCount !== 1 ? "s" : "" }} para
            enviar</span
          >
          <button
            @click="clearDone"
            class="text-[#05d16e] font-semibold cursor-pointer bg-transparent"
            style="border: none; padding: 0"
          >
            Limpiar enviadas
          </button>
        </div>
        <button
          @click="submitAll"
          :disabled="pendingCount === 0 || isUploading"
          :class="[
            'w-full flex items-center justify-center gap-3 py-4 rounded-2xl font-bold text-base cursor-pointer transition-transform active:scale-[.97]',
            pendingCount === 0 || isUploading
              ? 'bg-white/10 text-white/30 cursor-not-allowed'
              : 'bg-[#05d16e] text-[#024653]',
          ]"
          style="border: none"
        >
          <span
            v-if="isUploading"
            class="w-5 h-5 border-2 border-[#024653]/40 border-t-[#024653] rounded-full animate-spin"
          ></span>
          <svg
            v-else
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
          >
            <polyline points="16 16 12 12 8 16" />
            <line x1="12" y1="12" x2="12" y2="21" />
            <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
          </svg>
          {{
            isUploading
              ? "Enviando..."
              : `Clasificar ${pendingCount} imagen${pendingCount !== 1 ? "es" : ""}`
          }}
        </button>
      </div>
    </div>
    <!-- /MOBILE -->

    <!-- ═══════════════════════════════════════════
         DESKTOP LAYOUT
    ═══════════════════════════════════════════ -->
    <div class="hidden md:flex w-full max-w-lg flex-col gap-5">
      <!-- Header desktop -->
      <div class="flex flex-col gap-2">
        <span
          class="text-[.72rem] font-semibold tracking-widest uppercase text-[#cdff10] bg-[#cdff10]/10 px-3 py-1 rounded-full w-fit"
        >
          Paso 2 de 2
        </span>
        <h2 class="text-2xl font-bold text-white">Sube tus imágenes</h2>
        <p class="text-sm text-white/55">
          Hola, <strong class="text-[#05d16e]">{{ user.nombre }}</strong>
          {{ user.matricula ? ` (${user.matricula})` : "" }}. Puedes subir
          varias imágenes a la vez.
        </p>
      </div>

      <!-- Dropzone desktop -->
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
            o haz clic para seleccionar · máx. 8 MB por imagen
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

      <!-- Queue desktop -->
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
          <div class="w-12 h-12 rounded-lg overflow-hidden flex-shrink-0">
            <img
              :src="item.preview"
              :alt="item.file.name"
              class="w-full h-full object-cover"
            />
          </div>
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
                item.sizeError ? "⚠ Supera 8 MB" : formatSize(item.file.size)
              }}
            </span>
            <!-- Resultado clasificación desktop -->
            <div
              v-if="item.status === 'done'"
              class="flex items-center gap-2 mt-0.5 flex-wrap"
            >
              <span
                class="text-[.78rem] font-bold text-[#05d16e] bg-[#05d16e]/12 px-2 py-0.5 rounded-full"
              >
                {{ translateClass(item.result.class) }}
              </span>
              <span class="text-[.75rem] text-[#cdff10]">
                {{ (item.result.confidence * 100).toFixed(1) }}%
              </span>
              <span
                v-if="item.corrected"
                class="text-[.7rem] text-white/35 bg-white/[.06] px-1.5 py-0.5 rounded-full"
              >
                ✓ Corregida
              </span>
            </div>
            <div
              v-if="item.status === 'error'"
              class="text-[.75rem] text-red-400 mt-0.5"
            >
              {{ item.errorMsg }}
            </div>
            <div
              v-if="item.status === 'loading'"
              class="w-full h-[3px] bg-white/10 rounded-full mt-1 overflow-hidden"
            >
              <div
                class="h-full w-2/5 bg-[#cdff10] rounded-full progress-anim"
              ></div>
            </div>
          </div>

          <!-- Acciones desktop: Corregir o Eliminar -->
          <div class="flex items-center gap-1 flex-shrink-0">
            <!-- Botón corregir clasificación (solo cuando está done) -->
            <button
              v-if="item.status === 'done'"
              @click.stop="openCorrectionModal(item)"
              title="Corregir clasificación"
              class="p-1.5 rounded-lg text-white/35 hover:text-[#05d16e] hover:bg-[#05d16e]/10 transition-colors cursor-pointer"
              style="border: none; background: transparent"
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
              >
                <path
                  d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                />
                <path
                  d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                />
              </svg>
            </button>
            <!-- Botón eliminar (pending / error) -->
            <button
              v-if="item.status === 'pending' || item.status === 'error'"
              class="text-white/35 p-1.5 rounded-full hover:text-red-400 hover:bg-red-400/10 transition-colors cursor-pointer"
              style="border: none; background: transparent"
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
            <!-- Check done (sin botón de corregir visible, ya está el lápiz arriba) -->
            <div v-if="item.status === 'done'" class="p-1">
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
        </div>
      </TransitionGroup>

      <!-- Actions desktop -->
      <div
        v-if="queue.length"
        class="flex items-center justify-between gap-4 flex-wrap"
      >
        <span class="text-xs text-white/45">
          {{ pendingCount }} imagen{{ pendingCount !== 1 ? "es" : "" }} lista{{
            pendingCount !== 1 ? "s" : ""
          }}
          para enviar
        </span>
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
              'flex items-center gap-2 py-2 px-5 rounded-lg text-[#024653] font-semibold text-sm cursor-pointer transition-all duration-200',
              pendingCount === 0 || isUploading
                ? 'bg-[#1a4a3a] text-[#3a6a5a] cursor-not-allowed'
                : 'bg-[#05d16e] hover:bg-[#08b662] hover:shadow-[0_0_0_4px_rgba(5,209,110,.2)] active:scale-[.97]',
            ]"
            style="border: none"
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

      <!-- Restart desktop -->
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
    <!-- /DESKTOP -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const props = defineProps({ user: Object });
defineEmits(["restart"]);

const fileInput = ref(null);
const cameraInput = ref(null);
const queue = ref([]);
const dragging = ref(false);
const isUploading = ref(false);
const hasCamera = ref(false);
const showCorrectionModal = ref(false);
const itemToCorrect = ref(null);
const selectedClass = ref("");
const isCorrecting = ref(false);
const correctionError = ref("");
let idCounter = 0;

// ─── Traducciones de clases ───────────────────────────────────────────────────
const CLASS_LABELS = {
  crushed_metal: "Metal aplastado",
  crushed_plastic: "Plástico aplastado",
  metal: "Metal",
  no_reciclable: "No reciclable",
  plastic: "Plástico",
};

function translateClass(cls) {
  return CLASS_LABELS[cls] ?? cls ?? "—";
}

// Clases disponibles para el select de corrección
const availableClasses = Object.entries(CLASS_LABELS).map(([value, label]) => ({
  value,
  label,
}));

// ─── Detección de cámara ──────────────────────────────────────────────────────
onMounted(async () => {
  try {
    if (navigator.mediaDevices?.enumerateDevices) {
      const devices = await navigator.mediaDevices.enumerateDevices();
      hasCamera.value = devices.some((d) => d.kind === "videoinput");
    }
  } catch {
    hasCamera.value = false;
  }
});

function openCamera() {
  cameraInput.value.click();
}

// ─── Queue ────────────────────────────────────────────────────────────────────
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
    sizeError: file.size > 8 * 1024 * 1024,
    result: null,
    errorMsg: "",
    driveFileId: null,
    corrected: false,
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

// ─── Clasificación ────────────────────────────────────────────────────────────
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
        item.driveFileId = data.drive_file_id;
      }
    } catch {
      item.status = "error";
      item.errorMsg = "Error de conexión.";
    }
  }
  isUploading.value = false;
}

// ─── Modal de corrección ──────────────────────────────────────────────────────
function openCorrectionModal(item) {
  itemToCorrect.value = item;
  selectedClass.value = item.result?.class ?? "";
  correctionError.value = "";
  showCorrectionModal.value = true;
}

function closeCorrectionModal() {
  showCorrectionModal.value = false;
  itemToCorrect.value = null;
  selectedClass.value = "";
  correctionError.value = "";
}

async function submitCorrection() {
  if (!itemToCorrect.value || !selectedClass.value) return;
  isCorrecting.value = true;
  correctionError.value = "";

  try {
    const res = await fetch("/api/correct/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: itemToCorrect.value.driveFileId,
        type: selectedClass.value,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      correctionError.value = Object.values(data).flat().join(" ");
    } else {
      // Actualizar la clase en el item local
      itemToCorrect.value.result.class = selectedClass.value;
      itemToCorrect.value.corrected = true;
      closeCorrectionModal();
    }
  } catch {
    correctionError.value = "Error de conexión al corregir la clasificación.";
  } finally {
    isCorrecting.value = false;
  }
}
</script>

<style scoped>
.progress-anim {
  animation: progress 1.4s ease-in-out infinite;
}
@keyframes progress {
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(150%);
  }
  100% {
    transform: translateX(150%);
  }
}

/* Transición del modal */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active > div,
.fade-leave-active > div {
  transition: transform 0.25s cubic-bezier(0.34, 1.1, 0.64, 1);
}
.fade-enter-from > div {
  transform: translateY(24px) scale(0.97);
}
.fade-leave-to > div {
  transform: translateY(12px) scale(0.98);
}

/* Transiciones de la lista */
.list-enter-active,
.list-leave-active {
  transition: all 0.25s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(16px);
}
</style>
