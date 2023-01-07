<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStoreFile } from '@/stores/file';
import { useStoreURL } from  '@/stores/URL';

const router = useRouter();
const file = useStoreFile();
const domain = useStoreURL();

const loading = ref(false);
const uploadedFile = ref('');
const fileURL = ref('');
const radio = ref('solo');


// アップロードされたときの処理
const handleChangeFile = (e) => {
  uploadedFile.value = e.target.files[0];
  file.name = e.target.files[0].name;
  console.log(file.name);
  // file参照のための一時的なURLを生成
  fileURL.value = URL.createObjectURL(uploadedFile.value);
}


const uploading = async() => {

  const formData = new FormData();
  formData.append('upload_file', uploadedFile.value);
  
  // ローディング画面用
  loading.value = true;

  // post
  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

  // query
  const query = 'objective=' + radio.value
  const URL =  domain.getURL() + 'uploadfile?' + query
  console.log(URL);

  axios.post(URL, formData)
      .then(res => {
          loading.value = false;
          console.log(res.data);
          const ans = res.data;

          // データを受け取ったらページ遷移
          router.push({ path: 'result', query: { ans }});
      })
      .catch(error => {
          loading.value = false;
          console.log(error);
      })
}
</script>


<template>
  <div v-cloak>
    <transition-group
        name="fade"
        mode="out-in"
    >
      <div v-show="loading" class="loader" key="loader">
        <div id="loading">
          <div class="d-flex justify-content-center text-white mt-5">
            解析には数分かかる場合があります
            しばらくお待ちください
          </div>
          <div class="loading">
            <div class="obj"></div>
            <div class="obj"></div>
            <div class="obj"></div>
            <div class="obj"></div>
            <div class="obj"></div>
            <div class="obj"></div>
            <div class="obj"></div>
            <div class="obj"></div>
          </div>
        </div>
      </div>

      <!-- loading falseのとき -->
      <div v-show="!loading" key="notloader">
          <div class="card border-0">
            <img class="card-img rounded-0" src="../assets/img/sunset_blurred.jpg" alt="">
            <div class="card-img-overlay text-light">
              <p class="m-5">
                  <h1 class="m-3">耳コピのおともに</h1>
                  <p>特定の和音部分を切り出したファイル解析を行います</p>
              </p>

              <div class="container">
                <div class="row justify-content-center m-5">            
                  <!-- ファイル選択 -->
                  <div class="container m-5">
                      <div class="row justify-content-center m-3">
                          解析するファイルを選択してください (mp3, wavファイルのみ可)
                          <p>ファイル切り出しにおすすめのサイト：https://mp3cut.net/ja/</p>
                      </div>
                      <div class="input-group mb-3">
                          <input type="file" class="form-control" accept=".wav, .mp3" @change="handleChangeFile">
                      </div>
                  </div>

                  <div v-if="fileURL" class="container m-3">
                    <!-- 確認用の再生ボタン -->
                    <div class="row justify-content-center m-3">
                      選択したファイル（和音）を再生して確認してください
                    </div>
                    <div class="row justify-content-center mb-5">
                        <audio controls :src="fileURL"></audio>
                    </div>

                    <!-- クリックでページ遷移 -->
                    <div v-if="uploadedFile" class="d-flex justify-content-center m-5">
                      <input @click="uploading" class="btn btn-light" type="button" value="解析する" />
                    </div>
                  </div>
                </div>
              </div> 
            </div>
          </div>
      </div>
    </transition-group>
  </div>
</template>


<style scoped>
/* カードの上に文字 */
.card-img-overlay{
  padding: 0;
  /* top: calc(50% - 0.5rem); */
  text-align: center;
  font-weight: bold;
}

/* ローディング画面 */
.loader {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 1080;
}

#loading {
  width: 100vw;
  height: 100vh;
  transition: all 1s;
  background: rgba(0,0,0,1.0);
  position: absolute;
  left: 0;
  top: 0;
}
.loading{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    height: 40px;
    display: flex;
    align-items: center;
}
.obj{
    width: 5px;
    height: 60px;
    background: white;
    margin: 0 3px;
    border-radius: 10px;
    animation: loading 0.8s infinite;
}
.obj:nth-child(2){
    animation-delay: 0.1s;
}
.obj:nth-child(3){
    animation-delay: 0.2s;
}
.obj:nth-child(4){
    animation-delay: 0.3s;
}
.obj:nth-child(5){
    animation-delay: 0.4s;
}
.obj:nth-child(6){
    animation-delay: 0.5s;
}
.obj:nth-child(7){
    animation-delay: 0.6s;
}
.obj:nth-child(8){
    animation-delay: 0.7s;
}

@keyframes loading{
    0%{
        height: 0;
    }
    50%{
        height: 60px;
    }
    100%{
        height: 0;
    }
}
</style>
