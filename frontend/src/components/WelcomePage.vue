<template>
  <div
    class="min-h-screen flex flex-col relative z-10 md:items-center md:justify-center md:px-4 md:py-12"
  >
    <div class="absolute inset-0 md:hidden pointer-events-none">
      <div
        class="absolute top-0 left-0 right-0 h-[55%] bg-gradient-to-br from-[#05d16e]/20 via-[#024653] to-transparent"
      ></div>
      <div
        class="absolute bottom-0 left-0 right-0 h-[50%] bg-gradient-to-t from-[#021a20] to-transparent"
      ></div>
    </div>

    <div class="flex flex-col flex-1 md:hidden relative z-10">
      <div
        class="flex-1 flex flex-col items-center justify-center px-6 pt-16 pb-8"
      >
        <div class="w-24 h-24 relative mb-5">
          <svg
            viewBox="0 0 80 80"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="w-full h-full"
          >
            <circle
              cx="40"
              cy="40"
              r="38"
              stroke="#05d16e"
              stroke-width="1.5"
              stroke-dasharray="6 4"
              class="spin-slow"
            />
            <circle
              cx="40"
              cy="40"
              r="28"
              stroke="#05d16e"
              stroke-width="0.5"
              opacity="0.3"
            />
          </svg>
          <img
            src="/images/logo.png"
            alt="logo"
            class="absolute inset-0 m-auto w-14 h-14 object-contain"
          />
        </div>
        <h1
          class="text-6xl font-bold tracking-[.35em] text-white font-[stella] mb-2"
        >
          RENOVA
        </h1>
        <p
          class="text-[#05d16e] text-sm font-medium tracking-widest uppercase text-center"
        >
          Clasificación de materiales
        </p>

        <div class="flex gap-3 mt-8">
          <div
            class="flex flex-col items-center bg-white/[.06] border border-white/10 rounded-2xl px-5 py-3"
          >
            <span class="text-lg font-bold text-[#cdff10]">5</span>
            <span
              class="text-[.65rem] text-white/40 uppercase tracking-wider mt-0.5"
              >categorías</span
            >
          </div>
          <div
            class="flex flex-col items-center bg-white/[.06] border border-white/10 rounded-2xl px-5 py-3"
          >
            <span class="text-lg font-bold text-[#cdff10]">IA</span>
            <span
              class="text-[.65rem] text-white/40 uppercase tracking-wider mt-0.5"
              >modelo</span
            >
          </div>
          <div
            class="flex flex-col items-center bg-white/[.06] border border-white/10 rounded-2xl px-5 py-3"
          >
            <span class="text-lg font-bold text-[#cdff10]">100%</span>
            <span
              class="text-[.65rem] text-white/40 uppercase tracking-wider mt-0.5"
              >gratis</span
            >
          </div>
        </div>
      </div>

      <div class="px-6 pb-10 flex flex-col gap-3">
        <p class="text-center text-white/50 text-xs leading-relaxed px-4 mb-2">
          Ayúdanos a mejorar el dataset subiendo fotos de materiales
          reciclables.
        </p>
        <button
          @click="$emit('next')"
          class="w-full flex items-center justify-center gap-3 py-4 rounded-2xl bg-[#05d16e] text-[#024653] font-bold text-base cursor-pointer border-none active:scale-[.97] transition-transform"
        >
          Comenzar a contribuir
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

    <div class="hidden md:flex w-full max-w-md flex-col items-center gap-8">
      <div class="flex flex-col items-center gap-3">
        <div class="w-20 h-20 relative">
          <svg
            viewBox="0 0 80 80"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="w-full h-full"
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
          </svg>
          <img
            src="/images/logo.png"
            alt="logo"
            class="absolute inset-0 m-auto w-14 h-14 object-contain"
          />
        </div>
        <h1
          class="text-5xl font-bold tracking-[.45em] text-white font-[stella]"
        >
          RENOVA
        </h1>
      </div>

      <div
        class="w-full bg-white/[.04] border border-white/[.09] rounded-2xl backdrop-blur-xl p-10 text-center"
      >
        <p class="text-lg font-semibold text-[#05d16e] mb-3">
          Ayúdanos a identificar materiales reciclables
        </p>
        <p class="text-sm text-white/60 leading-relaxed mb-7 text-justify">
          Sube imágenes de materiales y nuestro modelo de inteligencia
          artificial los clasificará automáticamente. Tu participación nos ayuda
          a mejorar y contribuye a un futuro más sostenible.
        </p>
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
