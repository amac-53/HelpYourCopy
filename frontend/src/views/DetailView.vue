<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useStoreFile } from '@/stores/file';
import { useStoreURL } from '@/stores/URL';

const route = useRoute();
const file = useStoreFile();
const domain = useStoreURL();
console.log(file.name);

// 楽器ごとの情報取得のために使用する
const instrument = route.params['id'];
const URL = domain.getURL();
</script>

<template>
    <!-- 何の楽器かを示す -->
    <div class="text-white text-center fs-1 m-5">
        {{ instrument }} の詳細
    </div>

    <!-- 分割された音源の表示 -->
    <div v-if=" URL +'detail/split_file?objective=' + instrument + '&filename=' + file.name" class="container">
        <div class="row justify-content-center text-white">
            分割された音源
        </div>
        <div class="row justify-content-center mt-3 mb-5">
            <audio class="col-md-8" controls :src="URL +'detail/split_file?objective=' + instrument + '&filename=' + file.name"></audio>
        </div>
    </div>

    <!-- クロマグラムの表示 -->
    <div class="container pb-5">
        <div class="row justify-content-center text-white">
            <div v-if="URL +'detail/chromagram?instrument=' + instrument" class="d-flex justify-content-center">
                <img :src="URL +'detail/chromagram?instrument=' + instrument" alt="" class="w-auto">
            </div>
            <div v-else>
                音が存在しないようです
            </div>
        </div>
    </div>

    <!-- スペクトラムの表示 -->
    <div class="container pb-5">
        <div class="row justify-content-center text-white">
            <div v-if="URL +'detail/spectrum?instrument=' + instrument" class="d-flex justify-content-center">
                <img :src="URL +'detail/spectrum?instrument=' + instrument" alt="" class="w-auto">
            </div>
            <div v-else>
                音が存在しないようです
            </div>
        </div>
    </div>
</template>