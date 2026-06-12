<template>
  <div class="min-h-screen bg-bgcolor px-4 py-6 sm:px-8">
    <div class="mx-auto h-full w-full max-w-[920px] rounded-[67px] bg-displaybgcolor px-7 pb-10 pt-10 font-spotify text-white sm:px-10">
      <div class="flex flex-wrap items-end justify-between gap-4 border-b border-white/20 pb-5">
        <div>
          <p class="text-[36px] leading-none">PartyFy</p>
          <p class="mt-3 text-[20px] text-white/80">Party playlist</p>
        </div>
        <button
          type="button"
          @click="isOpen = true"
          class="rounded-[38px] bg-spoti px-5 py-2 text-[22px] text-white transition duration-500 hover:text-black"
        >
          Add Song
        </button>
      </div>

      <div class="mt-6 rounded-[24px] border border-white/10 bg-black/35 px-5 py-4">
        <p class="text-sm uppercase tracking-wide text-white/60">Invite link</p>
        <button
          type="button"
          @click="copyInviteLink"
          class="mt-2 rounded-[38px] bg-spoti px-4 py-2 text-[16px] text-white transition duration-300 hover:text-black"
        >
          Copy invite link
        </button>
        <p v-if="copyStatus === 'success'" class="mt-2 text-sm text-spoti">Link copied to clipboard</p>
        <p v-else-if="copyStatus === 'error'" class="mt-2 text-sm text-red-400">Unable to copy link</p>
      </div>

      <div v-if="songs.length" class="mt-6 flex flex-col gap-4">
        <PlaylistItem
          v-for="(song, index) in songs"
          :key="song.s3_name"
          :song="song"
          :isActive="index === currentIndex"
          :isDeleting="removingSongId === (song.id ?? song.s3_name)"
          @select-song="selectSong(index)"
          @remove-song="removeSong(song, index)"
        />
      </div>
      <div v-else class="mt-6 rounded-[24px] border border-dashed border-white/25 bg-black/25 px-6 py-12 text-center text-white/75">
        No songs yet in this party. Add the first track.
      </div>

      <div class="mt-8 rounded-[24px] border border-white/10 bg-black/45 px-5 py-4">
        <p class="text-xs uppercase tracking-wide text-white/50">Now playing</p>
        <div class="mt-2 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p class="text-[20px] leading-tight">{{ currentSongTitle }}</p>
            <p class="mt-1 text-sm text-grayspoti">{{ currentSongArtist }}</p>
          </div>

          <div class="flex items-center gap-3">
            <button
              type="button"
              @click="togglePlay"
              :disabled="!songs.length"
              class="flex h-11 w-11 items-center justify-center rounded-full bg-spoti text-white transition duration-500 hover:text-black disabled:cursor-not-allowed disabled:opacity-50"
              :aria-label="isPlaying ? 'Pause' : 'Play'"
            >
              <span v-if="!isPlaying" class="ml-[2px] inline-block h-0 w-0 border-y-[8px] border-y-transparent border-l-[13px] border-l-current"></span>
              <span v-else class="inline-flex gap-[3px]">
                <span class="h-4 w-[4px] rounded-sm bg-current"></span>
                <span class="h-4 w-[4px] rounded-sm bg-current"></span>
              </span>
            </button>
            <button
              type="button"
              @click="playNext"
              :disabled="!songs.length"
              class="rounded-[38px] border border-white/25 bg-black/30 px-4 py-2 text-[18px] text-white transition duration-300 hover:border-spoti disabled:cursor-not-allowed disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>

        <div class="mt-4">
          <input
            type="range"
            min="0"
            :max="duration || 0"
            :value="currentTime"
            @input="onSeekInput"
            :disabled="!songs.length || !duration"
            class="w-full accent-spoti disabled:opacity-40"
          />
          <div class="mt-1 flex items-center justify-between text-xs text-white/60">
            <span>{{ formatTime(currentTime) }}</span>
            <span>{{ formatTime(duration) }}</span>
          </div>
        </div>

        <div class="mt-3 flex items-center gap-3">
          <span class="text-xs uppercase tracking-wide text-white/60">Volume</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            :value="volume"
            @input="onVolumeInput"
            class="w-full max-w-[220px] accent-spoti"
          />
        </div>
      </div>

      <audio
        ref="audioPlayer"
        :src="currentAudioUrl"
        class="hidden"
        @ended="playNext"
        @timeupdate="onTimeUpdate"
        @loadedmetadata="onLoadedMetadata"
        @durationchange="onLoadedMetadata"
      ></audio>

  
      <AddSongPopup
        :isOpen="isOpen"
        :isSubmitting="isAddingSong"
        @close="isOpen = false"
        @submit="addSong"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onBeforeUnmount, ref } from "vue"
import { useRoute } from "vue-router"
import api from "../api/api.js"
import AddSongPopup from "./AddSongPopup.vue"
import PlaylistItem from "./PlaylistItem.vue"

const isOpen = ref(false)
const isAddingSong = ref(false)
const songs = ref([])
const currentIndex = ref(-1)
const isPlaying = ref(false)
const currentAudioUrl = ref("")
const audioPlayer = ref(null)
const audioUrlCache = ref({})
const removingSongId = ref(null)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(0.8)
const copyStatus = ref("")
const wsConnection = ref(null)
const wsReconnectTimer = ref(null)

const route = useRoute()
const partyUuid = route.params.uuid
const inviteLink = `http://127.0.0.1:5173/invitation/${partyUuid}`

const currentSong = computed(() => songs.value[currentIndex.value] || null)
const currentSongTitle = computed(() => currentSong.value?.item_name || "Choose a song")
const currentSongArtist = computed(() => currentSong.value?.artist_name || "No track selected")

const resetPlayerState = () => {
  if (audioPlayer.value) {
    audioPlayer.value.pause()
  }

  currentIndex.value = -1
  currentAudioUrl.value = ""
  currentTime.value = 0
  duration.value = 0
  isPlaying.value = false
}

const addSongIfNotExists = (song) => {
  if (!song) {
    return
  }

  const exists = songs.value.some((item) => {
    if (song.id && item.id) {
      return item.id === song.id
    }

    if (song.s3_name && item.s3_name) {
      return item.s3_name === song.s3_name
    }

    return false
  })

  if (!exists) {
    songs.value.push(song)
  }
}

const getSongUrl = async (song) => {
  if (audioUrlCache.value[song.s3_name]) {
    return audioUrlCache.value[song.s3_name]
  }

  const res = await api.get(`/items/get_url/${song.s3_name}`)
  const url = res.data.presigned_url
  audioUrlCache.value[song.s3_name] = url
  return url
}

const loadSongAtIndex = async (index) => {
  if (index < 0 || index >= songs.value.length) {
    return false
  }

  const song = songs.value[index]
  const url = await getSongUrl(song)

  currentIndex.value = index
  currentAudioUrl.value = url
  currentTime.value = 0
  duration.value = 0

  await nextTick()

  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value
  }

  return true
}

const startSong = async (index) => {
  if (index < 0 || index >= songs.value.length) {
    return
  }

  try {
    await loadSongAtIndex(index)
    await audioPlayer.value?.play()
    isPlaying.value = true
  } catch (err) {
    isPlaying.value = false
    console.error("Error loading audio:", err)
  }
}

const selectSong = async (index) => {
  if (index === currentIndex.value) {
    await togglePlay()
    return
  }

  await startSong(index)
}

const togglePlay = async () => {
  if (!songs.value.length) {
    return
  }

  if (currentIndex.value === -1) {
    await startSong(0)
    return
  }

  if (!audioPlayer.value) {
    return
  }

  if (audioPlayer.value.paused) {
    await audioPlayer.value.play()
    isPlaying.value = true
  } else {
    audioPlayer.value.pause()
    isPlaying.value = false
  }
}

const playNext = async () => {
  if (!songs.value.length) {
    return
  }

  const nextIndex = currentIndex.value === -1
    ? 0
    : (currentIndex.value + 1) % songs.value.length

  await startSong(nextIndex)
}

const onTimeUpdate = () => {
  if (!audioPlayer.value) {
    return
  }

  currentTime.value = audioPlayer.value.currentTime || 0
}

const onLoadedMetadata = () => {
  if (!audioPlayer.value) {
    return
  }

  duration.value = Number.isFinite(audioPlayer.value.duration)
    ? audioPlayer.value.duration
    : 0
}

const onSeekInput = (event) => {
  if (!audioPlayer.value) {
    return
  }

  const nextTime = Number(event.target.value)
  audioPlayer.value.currentTime = Number.isFinite(nextTime) ? nextTime : 0
  currentTime.value = audioPlayer.value.currentTime
}

const onVolumeInput = (event) => {
  const nextVolume = Number(event.target.value)
  volume.value = Number.isFinite(nextVolume) ? nextVolume : 0.8

  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value
  }
}

const copyInviteLink = async () => {
  copyStatus.value = ""

  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(inviteLink)
    } else {
      const textArea = document.createElement("textarea")
      textArea.value = inviteLink
      textArea.setAttribute("readonly", "")
      textArea.style.position = "absolute"
      textArea.style.left = "-9999px"
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand("copy")
      document.body.removeChild(textArea)
    }

    copyStatus.value = "success"
  } catch (error) {
    console.error("Copy failed:", error)
    copyStatus.value = "error"
  }
}

const formatTime = (seconds) => {
  if (!Number.isFinite(seconds) || seconds <= 0) {
    return "0:00"
  }

  const totalSeconds = Math.floor(seconds)
  const mins = Math.floor(totalSeconds / 60)
  const secs = totalSeconds % 60
  return `${mins}:${secs.toString().padStart(2, "0")}`
}

onMounted(async () => {
  try {
    const res = await api.get(`/party/get_full_party?party_uuid=${partyUuid}`)
    songs.value = res.data.items || []
    
    connectItemsWs()
  } catch (err) {
    console.error(err)
  }
})

onBeforeUnmount(() => {
  if (wsReconnectTimer.value) {
    clearTimeout(wsReconnectTimer.value)
    wsReconnectTimer.value = null
  }

  if (wsConnection.value) {
    try {
      wsConnection.value.close()
    } catch (e) {
      
    }
    wsConnection.value = null
  }
})


const connectItemsWs = () => {
  if (!partyUuid) return

  
  const host = '127.0.0.1:8000'
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
  const url = `${protocol}://${host}/ws/items/${partyUuid}`

  try {
    if (wsConnection.value) {
      try { wsConnection.value.close() } catch (e) {}
      wsConnection.value = null
    }

    const socket = new WebSocket(url)

    socket.onopen = () => {
      console.log('WS connected to', url)
      // clear any pending reconnection
      if (wsReconnectTimer.value) {
        clearTimeout(wsReconnectTimer.value)
        wsReconnectTimer.value = null
      }
    }

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data)

        if (!payload || !payload.type) return

        if (payload.type === 'item_added') {
          
          addSongIfNotExists(payload.data)
        }

        if (payload.type === 'item_removed') {
          const removedId = payload.data?.id
          if (!removedId) return
          const idx = songs.value.findIndex(it => (it.id && it.id === removedId) || (it.s3_name && it.s3_name === payload.data?.s3_name))
          if (idx !== -1) {
            const [removed] = songs.value.splice(idx, 1)
            if (removed?.s3_name) delete audioUrlCache.value[removed.s3_name]

          
            if (!songs.value.length) {
              resetPlayerState()
            } else if (idx < currentIndex.value) {
              currentIndex.value -= 1
            } else if (idx === currentIndex.value) {
              
              const nextIndex = Math.min(idx, songs.value.length - 1)
              loadSongAtIndex(nextIndex).catch(err => console.error(err))
            }
          }
        }
      } catch (err) {
        console.error('Invalid WS message', err)
      }
    }

    socket.onerror = (err) => {
      console.error('WS error:', err)
    }

    socket.onclose = (ev) => {
      console.warn('WS closed', ev)
      wsConnection.value = null
      
      if (wsReconnectTimer.value) clearTimeout(wsReconnectTimer.value)
      wsReconnectTimer.value = setTimeout(() => connectItemsWs(), 2000)
    }

    wsConnection.value = socket
  } catch (err) {
    console.error('Failed to initialize WS', err)
    // retry
    if (wsReconnectTimer.value) clearTimeout(wsReconnectTimer.value)
    wsReconnectTimer.value = setTimeout(() => connectItemsWs(), 2000)
  }
}

// Добавление песни
const addSong = async (url) => {
  isAddingSong.value = true

  try {
    const res = await api.post("/items/add_item", { url, party_uuid: partyUuid })
    .
    addSongIfNotExists(res.data)
    isOpen.value = false
  } catch (err) {
    console.error(err)
  } finally {
    isAddingSong.value = false
  }
}

const removeSong = async (song, index) => {
  if (!song || removingSongId.value) {
    return
  }

  removingSongId.value = song.id ?? song.s3_name ?? index

  const wasCurrentSong = index === currentIndex.value
  const wasPlaying = isPlaying.value && !audioPlayer.value?.paused

  try {
    await api.delete("/items/remove_item", {
      data: {
        id: song.id,
        party_uuid: partyUuid
      }
    })

    const removedIndex = songs.value.findIndex((item) => {
      if (song.id && item.id) {
        return item.id === song.id
      }

      if (song.s3_name && item.s3_name) {
        return item.s3_name === song.s3_name
      }

      return false
    })

    
    if (removedIndex === -1) {
      return
    }

    const [removedSong] = songs.value.splice(removedIndex, 1)

    if (removedSong?.s3_name) {
      delete audioUrlCache.value[removedSong.s3_name]
    }

    if (!songs.value.length) {
      resetPlayerState()
      return
    }

    if (removedIndex < currentIndex.value) {
      currentIndex.value -= 1
      return
    }

    if (wasCurrentSong) {
      const nextIndex = Math.min(removedIndex, songs.value.length - 1)

      if (wasPlaying) {
        await startSong(nextIndex)
      } else {
        await loadSongAtIndex(nextIndex)
      }
    }
  } catch (err) {
    console.error("Error removing song:", err)
  } finally {
    removingSongId.value = null
  }
}
</script>
