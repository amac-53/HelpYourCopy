<!-- アップロード部分 -->
<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const loading = ref(false);
const uploadedFile = ref('');
const fileURL = ref('');

// アップロードされたときの処理
const handleChangeFile = (e) => {
  uploadedFile.value = e.target.files[0];
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
  axios.post('http://127.0.0.1:8080/uploadfile/', formData)
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
            気長にお待ちください（すみません）
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
        <div class="container">
          <div class="d-flex justify-content-center">
            <h1>耳コピのおとも</h1>
          </div>
        </div>

        <!-- ファイル選択 -->
        <div class="container">
          <div class="row justify-content-center m-5">
            
            <!-- ファイル選択 -->
            <div class="container m-5">
                <div class="row justify-content-center m-3">
                    ファイルを選択してください
                </div>
                <div class="input-group mb-3">
                    <input type="file" class="form-control" accept=".wav, .mp3" @change="handleChangeFile">
                </div>
            </div>

            <!-- 確認用の再生ボタン -->
            <div v-if="fileURL" class="container m-5">
              <div class="row justify-content-center">
                確認用
              </div>
              <div class="row justify-content-center">
                  <audio controls :src="fileURL"></audio>
              </div>
            </div>

            <!-- クリックでページ遷移 -->
            <div v-if="uploadedFile" class="d-flex justify-content-center m-5">
              <input @click="uploading" class="btn btn-secondary" type="button" value="解析する" />
            </div>
          </div>
        </div>
      </div>
    </transition-group>
  </div>
</template>


<style scoped>
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
    height: 40px;
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
        height: 40px;
    }
    100%{
        height: 0;
    }
}
</style>
