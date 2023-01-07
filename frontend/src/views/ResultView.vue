<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';
import { useStoreFile } from '@/stores/file';

const route = useRoute();
const file = useStoreFile();

console.log(file.name);
const res = route.query;
// console.log(res);
</script>


<template>

    <!-- コードの候補を示す -->
    <div class="d-flex justify-content-center m-5">
        <div v-if="res" class="text-center text-white">
            最も可能性の高いコードは
            <h1 class="m-4"> {{ res['ans'] }} </h1>
            でした
        </div>
        <h4 v-else>
            適切なコードが定まりませんでした．
            詳細をご確認ください．
        </h4>
    </div>

    <!-- ベース・ピアノ・その他の楽器の詳細 -->
    <div class="d-flex justify-content-center m-5 text-white">
        詳細は以下ページからご確認ください
    </div>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-4">
                <RouterLink to="/detail/bass" class="text-decoration-none">
                    <div class="card border border-light bg-secondary text-white b p-2" style="max-height: 500px;">
                        <div class="row">
                            <div class="col-md-4">
                                <img src="@/assets/img/music_base.png" alt="" class="card-img" style="height: 200px;">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h4 class="card-title">Bass Info</h4>
                                    <p class="card-text">
                                        ベースの詳細情報（分離ファイル・クロマグラム）を確認できます
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </RouterLink>
            </div>
            <div class="col-4">
                <RouterLink to="/detail/piano" class="text-decoration-none">
                    <div class="card border border-light bg-secondary text-white p-2" style="max-height: 500px;">
                        <div class="row">
                            <div class="col-md-4">
                                <img src="../assets/img/music_piano.png" alt="" class="card-img" style="height: 200px;">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h4 class="card-title">Piano Info</h4>
                                    <p class="card-text">
                                        ピアノ（キーボード）の詳細情報（分離ファイル・クロマグラム）を確認できます
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </RouterLink>
            </div>
            <div class="col-4">
                <RouterLink to="/detail/other" class="text-decoration-none">
                <div class="card border border-light bg-secondary text-white p-2" style="max-height: 500px;">
                    <div class="row">
                        <div class="col-md-4">
                            <img src="../assets/img/music_guitar.png" alt="" class="card-img" style="height: 200px;">
                        </div>
                        <div class="col-md-8">
                            <div class="card-body">
                                <h4 class="card-title">Other Info</h4>
                                <p class="card-text">
                                    ギター・ストリングスの詳細情報（分離ファイル・クロマグラム）を確認できます
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                </RouterLink>
            </div>
        </div>
    </div>

</template>