<template>
  <div class="h-screen">
    <div class ="w-full h-full bg-bgcolor">
      <div class="w-1/3 rounded-[67px] mx-auto h-full bg-displaybgcolor">
        <div class="pt-10">
          <p class="flex justify-center text-white text-[64px] font-spotify ">
            PartyFY
          </p>
        </div>
        <div class="mb-30">
          <p class="flex justify-center text-white text-[32px] font-spotify ">
            Registration
          </p>
        </div>
        <div class="ml-20 mr-20">

          <form @submit.prevent="register" class="w-full flex flex-col gap-2">

            <label class="text-white font-spotify" for="username">Username</label>
            <input
                id="username"
                type="text"
                v-model="username"

                class="w-full font-spotify text-white px-4 pt-2 py-1 bg-grayspoti border border-white rounded-[38px]"
            >
            <p v-if="errors.username" class="text-red-500 text-sm">
              {{ errors.username }}
            </p>

            <label class="text-white font-spotify" for="email">Email</label>
            <input
                id="email"
                type="email"
                v-model="email"

                class="w-full font-spotify text-white px-4 pt-2 py-1 bg-grayspoti border border-white rounded-[38px]"
            >
            <p v-if="errors.email" class="text-red-500 text-sm">
              {{ errors.email }}
            </p>

            <label class="text-white font-spotify" for="password">Password</label>
            <input
                id="password"
                type="password"
                v-model="password"

                
                class="w-full font-spotify text-white px-4 pt-2 py-1 bg-grayspoti border border-white rounded-[38px]"
            >
            <p v-if="errors.password" class="text-red-500 text-sm">
              {{ errors.password }}
            </p>

            <p class="flex justify-center pt-6 text-white text-[16px] font-spotify">
              I have already registered:<router-link to="/login" class="btn"> login </router-link>
            </p>
            <button
                type="submit"
                class="cursor-pointer mt-3 mr-20 ml-20 py-1 px-1 bg-spoti font-spotify text-[36px] text-white rounded-[38px]"
            >
              Register
            </button>

          </form>



        </div>
      </div>
    </div>
  </div>

</template>



<script setup>
import { ref, computed } from 'vue'
import { useRouter } from "vue-router"

const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')

const errors = ref({
  username: '',
  email: '',
  password: ''
})

function validate() {
  let isValid = true

  // Сброс ошибок
  errors.value.username = ''
  errors.value.email = ''
  errors.value.password = ''

  // Username max 50
  if (username.value.length === 0) {
    errors.value.username = 'Username is required'
    isValid = false
  } else if (username.value.length > 50) {
    errors.value.username = 'Username must be less than 50 characters'
    isValid = false
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email.value) {
    errors.value.email = 'Email is required'
    isValid = false
  } else if (!emailRegex.test(email.value)) {
    errors.value.email = 'Invalid email format'
    isValid = false
  }

  // Password min 8
  if (!password.value) {
    errors.value.password = 'Password is required'
    isValid = false
  } else if (password.value.length < 8) {
    errors.value.password = 'Password must be at least 8 characters'
    isValid = false
  }

  return isValid
}

async function register() {


  if (!validate()) return

  const url = "http://127.0.0.1:8000/auth/register"

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
      })
    })

    if (!response.ok) {
      const result = await response.json()
      throw new Error(result.detail || `Status ${response.status}`)

    }
    else{
      router.push("/")
      const result = await response.json()
      console.log(result)
    }


  } catch (error) {
    console.error(error.message)
  }
}
</script>



<style scoped>

</style>
