<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';

const route = useRoute();
const res = route.query;
console.log(res);

</script>

<template>

    <!-- コードの候補を示す -->
    <div class="d-flex justify-content-center">
        <div v-if="res" class="text-center">
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
    <div class="d-flex justify-content-center m-5">
        詳細は以下ページからご確認ください
    </div>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-4">
                <RouterLink to="/detail/bass">
                    <div class="card bg-secondary text-white p-2" style="height: 220px;">
                        <div class="row">
                            <div class="col-4">
                                <img src="@/assets/music_base.png" alt="" class="card-img" style="height: 200px;">
                            </div>
                            <div class="col-8">
                                <div class="card-body">
                                    <h5 class="card-title">Bass Info</h5>
                                    <p class="card-text">ベースラインの詳細情報を提示します</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </RouterLink>
            </div>
            <div class="col-4">
                <RouterLink to="/detail/piano">
                    <div class="card bg-secondary text-white p-2" style="height: 220px;">
                        <div class="row">
                            <div class="col-4">
                                <img src="../assets/music_piano.png" alt="" class="card-img" style="height: 200px;">
                            </div>
                            <div class="col-8">
                                <div class="card-body">
                                    <h5 class="card-title">Piano Info</h5>
                                    <p class="card-text">ピアノの詳細情報を提示します</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </RouterLink>
            </div>
            <div class="col-4">
                <RouterLink to="/detail/other">
                <div class="card bg-secondary text-white p-2" style="height: 220px;">
                    <div class="row">
                        <div class="col-4">
                            <img src="../assets/music_guitar.png" alt="" class="card-img" style="height: 200px;">
                        </div>
                        <div class="col-8">
                            <div class="card-body">
                                <h5 class="card-title">Other Info</h5>
                                <p class="card-text">その他（ギターやストリングスなど）の詳細情報を提示します</p>
                            </div>
                        </div>
                    </div>
                </div>
                </RouterLink>
            </div>
        </div>
    </div>

</template>