<script setup lang="ts">
import { useRoute } from 'vue-router';

const route = useRoute();

// 楽器ごとの情報取得のために使用する
const instrument = route.params['id'];

</script>

<template>

    <!-- 何の楽器かを示す -->
    <div class="text-center fs-1 m-5">
        {{ instrument }}
    </div>
    <!-- クロマグラムの表示 -->
    <div class="container">
        <div class="row justify-content-center">
            <div v-if="'http://localhost:8080/detail/chromagram?instrument=' + instrument" class="d-flex justify-content-center">
                <img :src="'http://localhost:8080/detail/chromagram?instrument=' + instrument" alt="" class="w-auto">
            </div>
            <div v-else>
                音が存在しないようです
            </div>
        </div>
    </div>

    <!-- スペクトラムの表示 -->
    <div class="container">
        <div class="row justify-content-center">
            <div v-if="'http://localhost:8080/detail/spectrum?instrument=' + instrument" class="d-flex justify-content-center">
                <img :src="'http://localhost:8080/detail/spectrum?instrument=' + instrument" alt="" class="w-auto">
            </div>
            <div v-else>
                音が存在しないようです
            </div>
        </div>
    </div>
</template>