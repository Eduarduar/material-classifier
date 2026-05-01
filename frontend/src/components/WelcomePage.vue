<template>
  <div
    class="min-h-screen flex items-center justify-center px-4 py-12 relative z-10"
  >
    <div class="w-full max-w-md flex flex-col items-center gap-8">
      <!-- Logo -->
      <div class="flex flex-col items-center gap-3">
        <div class="w-20 h-20">
          <svg
            viewBox="0 0 80 80"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="40"
              cy="40"
              r="38"
              stroke="#05d16e"
              stroke-width="2"
              stroke-dasharray="6 4"
              class="spin-slow"
            />
            <path
              d="M40 14 A26 26 0 0 1 62 52 L54 48 L58 62 L44 56 L52 52 A18 18 0 0 0 40 22 Z"
              fill="#05d16e"
            />
            <path
              d="M40 66 A26 26 0 0 1 18 28 L26 32 L22 18 L36 24 L28 28 A18 18 0 0 0 40 58 Z"
              fill="#05d16e"
              opacity=".7"
            />
          </svg>
        </div>
        <h1 class="text-5xl font-bold tracking-[.2em] text-white">RENOVA</h1>
      </div>

      <!-- Card -->
      <div
        class="w-full bg-white/[.04] border border-white/[.09] rounded-2xl backdrop-blur-xl p-10 text-center"
      >
        <p class="text-lg font-semibold text-[#05d16e] mb-3">
          Ayúdanos a identificar materiales reciclables
        </p>
        <p class="text-sm text-white/60 leading-relaxed mb-7">
          Sube imágenes de materiales y nuestro modelo de inteligencia
          artificial los clasificará automáticamente. Tu participación mejora el
          dataset y contribuye a un futuro más sostenible.
        </p>

        <!-- Stats -->
        <div
          class="flex items-center justify-center gap-5 mb-8 p-5 bg-[#05d16e]/[.06] rounded-xl border border-[#05d16e]/[.15]"
        >
          <div class="flex flex-col items-center gap-1">
            <span class="text-xl font-bold text-[#cdff10]">5</span>
            <span class="text-[.7rem] text-white/50 uppercase tracking-widest"
              >categorías</span
            >
          </div>
          <div class="w-px h-8 bg-white/10"></div>
          <div class="flex flex-col items-center gap-1">
            <span class="text-xl font-bold text-[#cdff10]">IA</span>
            <span class="text-[.7rem] text-white/50 uppercase tracking-widest"
              >clasificación</span
            >
          </div>
          <div class="w-px h-8 bg-white/10"></div>
          <div class="flex flex-col items-center gap-1">
            <span class="text-xl font-bold text-[#cdff10]">100%</span>
            <span class="text-[.7rem] text-white/50 uppercase tracking-widest"
              >gratuito</span
            >
          </div>
        </div>

        <button
          @click="$emit('next')"
          class="w-full flex items-center justify-center gap-2 py-3 px-8 rounded-lg bg-[#05d16e] text-[#024653] font-semibold text-[.95rem] cursor-pointer border-none transition-all duration-200 hover:bg-[#08b662] hover:shadow-[0_0_0_4px_rgba(5,209,110,.2)] active:scale-[.97]"
        >
          Comenzar
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
  </div>
</template>

<script setup>
defineEmits(["next"]);
</script>
