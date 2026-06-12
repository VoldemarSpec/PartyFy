<script setup>
import { ref } from 'vue'

defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'submit'])

const partyname = ref('')

const submit = () => {
  emit('submit', partyname.value)
  partyname.value = ''
  emit('close')
}
</script>

<template>
  <div v-if="isOpen"
       class="fixed inset-0 bg-black/50 flex items-center justify-center"
       @click="emit('close')">

    <div class="rounded-[75px] bg-darkgray p-6"
         @click.stop>

      <slot />

      <form @submit.prevent="submit"
            class="w-full flex flex-col gap-2">

        <label class="text-white font-spotify">
          Party name
        </label>

        <input
            v-model="partyname"
            type="text"
            class="w-full font-spotify text-white px-4 pt-2 py-1 bg-grayspoti border border-white rounded-[38px]"
        >

        <button
            type="submit"
            class="cursor-pointer mt-3 mx-20 py-1 bg-spoti font-spotify text-[20px] text-white rounded-[38px] hover:bg-black transition">

          add party

        </button>

      </form>

    </div>

  </div>
</template>
