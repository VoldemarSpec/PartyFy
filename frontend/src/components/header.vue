<template>
  <div class="min-h-screen bg-bgcolor px-4 py-6 sm:px-8">
    <div class="mx-auto flex min-h-[calc(100vh-3rem)] w-full max-w-[620px] items-center justify-center">
      <div class="w-full rounded-[38px] bg-displaybgcolor px-5 py-8 sm:rounded-[67px] sm:px-10 sm:py-10">
        <div class="flex justify-end">
        <button @click="ToRegister"
            class="px-4 py-1 border-spoti border bg-black text-white rounded-[38px] text-[18px] font-spotify
             hover:bg-displaybgcolor cursor-pointer transition duration-500 sm:text-[24px]">
          sign up

        </button>
        </div>
        <div class="mt-6 text-[32px] text-white font-spotify sm:text-[36px]">
          <p>PartyFy</p>
        </div>
        <div class="text-[17px] text-white font-spotify mt-3 sm:text-[20px]">
          <p>Combine music tastes with your friends during <br> parties from different streaming services</p>
        </div>
         <div class="mt-7 flex justify-center">
        <img src="../assets/images/services.png" class="w-full max-w-[360px]">

      </div>
        <div class="mt-6">
          <button @click="ToParties" class="text-[20px] text-white font-spotify  bg-spoti py-2 px-5 rounded-[38px]
           hover:text-black cursor-pointer transition duration-500" >
            Start Right Now
          </button>
        </div>


      </div>


    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
const router = useRouter()


function ToParties() {
  router.push("/parties")
}

function ToRegister() {
  router.push("/registration")


}


</script>

<style>

</style>
