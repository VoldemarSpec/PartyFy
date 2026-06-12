<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4 backdrop-blur-sm"
    @click.self="closePopup"
  >
    <div class="w-full max-w-[520px] rounded-[26px] border border-white/15 bg-displaybgcolor px-6 py-5 font-spotify text-white shadow-2xl sm:px-7 sm:py-6">
      <p class="text-[28px] leading-none">Add Song</p>
      <p class="mt-2 text-sm text-white/65">Paste Spotify or track URL</p>

      <input
        v-model="songUrl"
        type="url"
        placeholder="https://..."
        class="mt-4 w-full rounded-[38px] border border-white/20 bg-black/35 px-4 py-2 text-white placeholder:text-white/45 outline-none transition duration-300 focus:border-spoti"
      />

      <div class="mt-5 flex justify-end gap-3">
        <button
          type="button"
          @click="closePopup"
          :disabled="isSubmitting"
          class="cursor-pointer rounded-[38px] border border-white/25 bg-black/30 px-4 py-2 text-[16px] text-white transition duration-300 hover:border-spoti"
        >
          Cancel
        </button>
        <button
          type="button"
          @click="submitSong"
          :disabled="!songUrl.trim() || isSubmitting"
          class="cursor-pointer rounded-[38px] bg-spoti px-5 py-2 text-[18px] text-white transition duration-300 hover:text-black disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ isSubmitting ? "Adding..." : "Add" }}
        </button>
      </div>

      <p v-if="isSubmitting" class="mt-3 text-sm text-white/75">Song is being added...</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

// props
const props = defineProps({
  isOpen: Boolean,
  isSubmitting: {
    type: Boolean,
    default: false
  }
})

// define emits
const emit = defineEmits(["close", "submit"])

const songUrl = ref("")

const closePopup = () => {
  if (props.isSubmitting) {
    return
  }

  emit("close")
}

const submitSong = () => {
  const value = songUrl.value.trim()
  if (!value || props.isSubmitting) return

  emit("submit", value)
  songUrl.value = ""
}
</script>