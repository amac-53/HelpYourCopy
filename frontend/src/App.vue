<!-- アップロード部分 -->
<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import "bootstrap/dist/css/bootstrap.min.css";
import AppHeader from "./components/AppHeader.vue"; 
import AppDetail from "./components/AppDetail.vue";

const data_ = reactive({
  prob_notes: {},
  notes: [],
  prob: [] 
});


const uploadFile = async(event) => {
  const formData = new FormData();
  formData.append('upload_file', event.target.files[0])

  // post
  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
  axios.post('http://127.0.0.1:8000/uploadfile/', formData)
      .then(res => {
          // console.log(res.data);
          // console.log(res.data.map(data => data.prob));
          data_.prob = res.data.map(data => data.prob);
          data_.notes = res.data.map(data => data.note);
          temp();
      })
      .catch(error => {
          console.log(error);
      })
}

const getChromagram = async() => {
    axios.get('http://127.0.0.1:8000/img/chromagram.png')
      .then(res =>{
        console.log(res);
      })
      .catch(error => {
        console.log(error);
      })
}

const getSpectrogram = async() => {
    axios.get('http://127.0.0.1:8000/getspectrogram/')
      .then(res =>{
      })
      .catch(error => {
        console.log(error);
      })
}


const temp = () => {
  const ctx = document.getElementById('myChart').getContext('2d');
  const myChart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: data_.notes,
          datasets: [{
              label: 'probability',
              data: data_.prob
          }]
      }
  });
}
// style="width:800px"
</script>


<template>
<AppHeader/>
<div class="input-group mb-3">
  <input type="file" class="form-control" accept=".wav, .mp3" @change="uploadFile">
</div>
<div class="container">
  <div class="row justify-content-md-center">
    <canvas id="myChart"></canvas>
  </div>
</div>
<AppDetail @click="getChromagram" chroma=data_.chroma_img />
<!-- <AppDetail @click="getSpectrogram" chroma=data_.chroma_img /> -->

</template>