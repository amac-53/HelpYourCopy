<script setup lang="ts">
import "bootstrap/dist/css/bootstrap.min.css";
import AppHeader from "./components/AppHeader.vue"; 
import AppFooter from "./components/AppFooter.vue"; 
import { RouterView } from "vue-router";
</script>


<template>
<AppHeader/>
<main>
<RouterView />
</main>
<AppFooter />
</template>