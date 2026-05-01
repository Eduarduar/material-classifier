<template>
  <div
    class="min-h-screen relative overflow-hidden bg-[#024653]"
    style="
      background:
        radial-gradient(
          ellipse at 20% 0%,
          rgba(5, 209, 110, 0.18) 0%,
          transparent 55%
        ),
        radial-gradient(
          ellipse at 80% 100%,
          rgba(205, 255, 16, 0.1) 0%,
          transparent 50%
        ),
        #024653;
    "
  >
    <Transition name="fade" mode="out-in">
      <WelcomePage v-if="step === 'welcome'" @next="step = 'form'" />
      <UserForm v-else-if="step === 'form'" @next="onFormDone" />
      <ImageUpload
        v-else-if="step === 'upload'"
        :user="user"
        @restart="restart"
      />
    </Transition>
  </div>
</template>

<script setup>
import { ref } from "vue";
import WelcomePage from "./components/WelcomePage.vue";
import UserForm from "./components/UserForm.vue";
import ImageUpload from "./components/ImageUpload.vue";

const step = ref("welcome");
const user = ref({});

function onFormDone(userData) {
  user.value = userData;
  step.value = "upload";
}
function restart() {
  user.value = {};
  step.value = "welcome";
}
</script>

<style>
@import "tailwindcss";

.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.22s ease,
    transform 0.22s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(18px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-18px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  margin: 0;
}
.slide-enter-to,
.slide-leave-from {
  max-height: 120px;
}

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
  transform: translateX(20px);
}

@keyframes spin-slow {
  to {
    transform: rotate(360deg);
  }
}
.spin-slow {
  animation: spin-slow 12s linear infinite;
  transform-origin: center;
}

@keyframes progress-anim {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(300%);
  }
}
.progress-anim {
  animation: progress-anim 1.2s ease-in-out infinite;
}
</style>
