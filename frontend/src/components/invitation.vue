<template>
  <div class="h-screen bg-bgcolor px-4 py-6 sm:px-8">
    <div class="mx-auto flex h-full w-full max-w-[620px] items-center justify-center">
      <div class="w-full rounded-[67px] bg-displaybgcolor px-7 pb-10 pt-10 sm:px-10">
        <div class="text-right">
          <button
            @click="goToHome"
            class="cursor-pointer rounded-[38px] border border-spoti bg-black px-4 py-1 text-[20px] text-white font-spotify transition duration-500 hover:bg-displaybgcolor"
          >
            Home
          </button>
        </div>

        <div class="mt-6 text-white font-spotify">
          <p class="text-[36px] leading-none">PartyFy</p>
          <p class="mt-3 text-[20px] text-white/85">You have been invited to a party</p>
        </div>

        <div class="mt-8 rounded-[26px] border border-white/10 bg-black/35 px-5 py-5 text-white font-spotify">
          <p class="text-sm uppercase tracking-wide text-white/60">Party code</p>
          <p class="mt-2 break-all text-[22px] leading-tight">{{ partyUuid }}</p>
          <p class="mt-3 text-[15px] text-white/70">
            Join the party playlist and add your tracks in one shared queue.
          </p>
          <p v-if="isLoading" class="mt-3 text-[14px] text-white/70">Authorizing invitation...</p>
          <p v-if="errorMessage" class="mt-3 text-[14px] text-red-400">{{ errorMessage }}</p>
        </div>

        <div class="mt-8 flex flex-wrap gap-3">
          <button
            @click="joinParty"
            :disabled="isLoading"
            class="cursor-pointer rounded-[38px] bg-spoti px-5 py-2 text-[22px] text-white font-spotify transition duration-500 hover:text-black"
          >
            {{ isLoading ? "Joining..." : "Join Party" }}
          </button>
          <button
            v-if="errorMessage"
            @click="joinParty"
            :disabled="isLoading"
            class="cursor-pointer rounded-[38px] border border-spoti bg-black px-5 py-2 text-[22px] text-white font-spotify transition duration-500 hover:bg-displaybgcolor"
          >
            Retry
          </button>
          <button
            @click="goToLogin"
            class="cursor-pointer rounded-[38px] border border-white/20 bg-black px-5 py-2 text-[22px] text-white font-spotify transition duration-500 hover:border-spoti"
          >
            Login
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import axios from "axios"

const route = useRoute()
const router = useRouter()

const partyUuid = computed(() => route.params.uuid || "unknown")
const isLoading = ref(false)
const errorMessage = ref("")

async function authorizeInvitation() {
  if (!partyUuid.value || partyUuid.value === "unknown") {
    errorMessage.value = "Invitation link is invalid."
    return false
  }

  // Инвайт использует cookie-auth, поэтому убираем потенциально устаревший bearer из localStorage.
  localStorage.removeItem("access_token")

  isLoading.value = true
  errorMessage.value = ""

  try {
    // Для инвайта используем прямой запрос без глобального interceptor,
    // чтобы старый/просроченный Bearer-токен не ломал публичный вход.
    const res = await axios.get(`http://127.0.0.1:8000/auth/invitation/${partyUuid.value}`, {
      withCredentials: true
    })

    // Бэкенд возвращает { message: "joined" } и ставит httpOnly cookie access_token.
    // Токен не читается из JS и не должен приходить в response body.
    if (res.data?.message && res.data.message !== "joined") {
      errorMessage.value = "Invitation response is not valid."
      return false
    }

    return true
  } catch (error) {
    console.error(error)

    const status = error?.response?.status
    const detail = error?.response?.data?.detail

    if (status === 404) {
      errorMessage.value = "Invitation not found or expired."
    } else if (status === 401) {
      errorMessage.value = "Invitation is not valid anymore."
    } else if (status === 422) {
      errorMessage.value = "Invalid invitation format."
    } else {
      errorMessage.value = detail || "Failed to authorize invitation. Please try again."
    }

    return false
  } finally {
    isLoading.value = false
  }
}

async function joinParty() {
  const ok = await authorizeInvitation()

  if (ok) {
    router.replace(`/party/${partyUuid.value}/items`)
  }
}

function goToLogin() {
  router.push("/login")
}

function goToHome() {
  router.push("/")
}

onMounted(async () => {
  await joinParty()
})
</script>

