<script setup lang="ts">
defineProps(['chroma']);
</script>

<template>
    <details>
        <summary>Detail data</summary>
        <div class="container">
        <div class="row">
        <div class="col-6">
            <img src="http://localhost:8000/img/chromagram.png" alt="">
        </div>
        <div class="col-6">
            <img src="http://localhost:8000/img/spectrum.png" alt="">
        </div>
        </div>
        </div>
    </details>
</template>