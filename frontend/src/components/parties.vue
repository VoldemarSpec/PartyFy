<template>
  <div class="h-screen bg-bgcolor px-4 py-6 sm:px-8">
    <div class="mx-auto flex h-full w-full max-w-[620px] items-center justify-center">
      <div class="relative h-full w-full rounded-[67px] bg-displaybgcolor px-7 pb-28 pt-10 sm:px-10">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-[40px] leading-none text-white font-spotify">PartyFy</p>
            <p class="mt-3 text-[20px] text-white/80 font-spotify">Your shared music space</p>
          </div>
          <div class="rounded-[28px] border border-white/20 bg-black/40 px-4 py-2 text-white font-spotify">
            {{ parties.length }}
          </div>
        </div>

        <div class="mt-8 flex items-end justify-between border-b border-white/20 pb-4">
          <p class="text-[32px] leading-none text-white font-spotify">Parties</p>
          <p class="text-sm text-white/60 font-spotify">Pick one to continue</p>
        </div>

        <div class="mt-6 max-h-[60vh] overflow-y-auto pr-1 custom-scroll">
          <div v-if="parties.length > 0" class="grid gap-3 pb-2">
            <button
              v-for="party in parties"
              :key="party.id"
              :data-uuid="party.uuid"
              @click="goToParty($event)"
              class="cursor-pointer flex items-center justify-between rounded-[22px] border border-white/10 bg-black/35 px-5 py-4 text-left text-white font-spotify transition duration-300 hover:border-spoti hover:bg-black/70 focus:outline-none focus:ring-2 focus:ring-spoti"
            >
              <span class="text-[20px]">{{ party.party_name }}</span>
              <span class="text-white/50">></span>
            </button>
          </div>

          <div v-else class="flex min-h-[300px] items-center justify-center rounded-[22px] border border-dashed border-white/25 bg-black/25 px-6 text-center text-[20px] text-white/80 font-spotify">
            Nothing here yet. Create your first party.
          </div>
        </div>

        <button
          @click="isOpen = true"
          class="cursor-pointer absolute bottom-8 left-1/2 -translate-x-1/2 rounded-[80px] bg-spoti px-7 py-3 text-[20px] text-white font-spotify transition duration-300 hover:bg-black"
        >
          Add party
        </button>

        <Popup
          :isOpen="isOpen"
          @close="isOpen = false"
          @submit="addParty"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import Popup from "./popup.vue"
import api from "../api/api"
import { onMounted, ref } from "vue"

const router = useRouter()
const isOpen = ref(false)
const parties = ref([])

onMounted(async () => {
  try {

    const response = await api.get("/party/get_parties")

    parties.value = response.data
  } catch (error) {
    console.error(error)
  }
})


const goToParty = (e) => {
  const uuid = e.currentTarget.dataset.uuid

  router.push(`/party/${uuid}/items`)
}

const addParty = async (partyname) => {
  try {

    const res = await api.post("/party/create_party", {
      party_name: partyname
    })

    parties.value.push(res.data)

  } catch (err) {
    console.error(err)
  }
}
</script>



<style scoped>
.custom-scroll::-webkit-scrollbar {
  width: 6px;
}

.custom-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scroll::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}
</style>