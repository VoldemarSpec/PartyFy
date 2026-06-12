import { createRouter, createWebHistory } from "vue-router"

import Registration from "../components/registraton.vue"
import About from "../components/header.vue"
import Login from "@/components/login.vue";
import Parties from "@/components/parties.vue";
import PartyItems from "@/components/PartyItems.vue";
import Invitation from "@/components/invitation.vue";
const routes = [
    { path: "/registration", component: Registration },
    { path: "/", component: About },
    { path: "/login", component: Login },
    { path: "/parties", component: Parties },
    { path: "/party/:uuid/items", component: PartyItems, props: true },
    { path: "/invitation/:uuid", component: Invitation, props: true }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router