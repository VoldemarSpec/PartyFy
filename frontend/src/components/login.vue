<template>
  <div class="min-h-screen bg-bgcolor px-4 py-6 sm:px-8">
    <div class="mx-auto flex min-h-[calc(100vh-3rem)] w-full max-w-[620px] items-center justify-center">
      <div class="w-full rounded-[38px] bg-displaybgcolor px-5 py-8 sm:rounded-[67px] sm:px-10 sm:py-10">
        <div>
          <p class="flex justify-center text-white text-[44px] leading-none font-spotify sm:text-[64px]">
            PartyFY
          </p>
        </div>
        <div class="mb-10 sm:mb-14">
          <p class="mt-2 flex justify-center text-white text-[26px] font-spotify sm:text-[32px]">
            Login
          </p>
        </div>
        <div class="mx-auto w-full max-w-[420px]">

          <form @submit.prevent="login" class="w-full flex flex-col gap-2">


            <label class="text-white font-spotify" for="email">Email</label>
            <input
                id="email"
                type="email"
                v-model="email"
                class="w-full font-spotify text-white px-4 pt-2 py-1 bg-grayspoti border border-white rounded-[38px]"
            >

            <label class="text-white font-spotify" for="password">Password</label>
            <input
                id="password"
                type="password"
                v-model="password"
                class="w-full font-spotify text-white px-4 pt-2 py-1 bg-grayspoti border border-white rounded-[38px]"
            >

            <p class="flex justify-center pt-6 text-white text-[16px] font-spotify">
              Dont have an account?<router-link to="/registration" class="btn"> Register </router-link>
            </p>
            <button
                type="submit"
                class="cursor-pointer mt-4 w-full py-2 px-2 bg-spoti font-spotify text-[28px] text-white rounded-[38px] sm:text-[36px]"
            >
              Login
            </button>

          </form>



        </div>
      </div>
    </div>
  </div>

</template>



<script setup>
import { ref } from 'vue'
import { useRouter } from "vue-router"

const router = useRouter()

const email = ref('')
const password = ref('')




async function login() {
  const url = "http://127.0.0.1:8000/auth/login"
  try{
    const response = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
            "email": email.value,
            "password": password.value,
          }
      )
    })
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    else{
      const result = await response.json();
      console.log(result);
      router.push({ path: `/parties` });

    }



  } catch (error) {
    console.error(error.message);
  }
}

</script>



<style scoped>

</style>