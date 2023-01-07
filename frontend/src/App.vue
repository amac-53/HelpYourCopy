<script setup lang="ts">
import AppHeader from "./components/AppHeader.vue"; 
import AppFooter from "./components/AppFooter.vue"; 
import { RouterView } from "vue-router";
import "bootstrap/dist/css/bootstrap.min.css";
</script>


<template>
    <div class="global">
        <AppHeader/>
        <main>
        <RouterView/>
        </main>
        <AppFooter/>
    </div>
</template>

