<template>
  <div
    class="rounded-[26px] border bg-displaybgcolor px-5 py-4 font-spotify text-white shadow-lg transition duration-300"
    :class="isActive ? 'border-spoti' : 'border-white/10 hover:border-spoti/60'"
  >
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p class="text-[22px] leading-tight">{{ song.item_name }}</p>
        <p class="mt-1 text-sm text-grayspoti">{{ song.artist_name }}</p>
        <p class="mt-2 text-xs uppercase tracking-wide text-white/50">added by {{ song.added_by_name }}</p>
      </div>

      <div class="flex items-center gap-3 sm:items-end">
        <button
          type="button"
          @click="$emit('select-song')"
          class="cursor-pointer rounded-[38px] bg-spoti px-4 py-1 text-[18px] text-white transition duration-500 hover:text-black focus:outline-none focus:ring-2 focus:ring-spoti"
        >
          {{ isActive ? "Playing" : "Play" }}
        </button>
        <button
          type="button"
          @click="$emit('remove-song')"
          :disabled="isDeleting"
          class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-white/15 bg-black/30 text-white transition duration-300 hover:border-red-400 hover:text-red-300 focus:outline-none focus:ring-2 focus:ring-red-400 disabled:cursor-not-allowed disabled:opacity-50"
          aria-label="Remove song"
          title="Remove song"
        >
          <span class="text-[22px] leading-none">×</span>
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
defineProps({
  song: {
    type: Object,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  },
  isDeleting: {
    type: Boolean,
    default: false
  }
})

defineEmits(["select-song", "remove-song"])
</script>