<template>
  <div class="article-detail-wrap" >
    <h1><img @click="goBack" src="@/assets/image/back.png"/>{{ article?.title }}</h1>
    <div class="detail-title"></div>
    <div class="detail-content-wrap" data-aos="fade-up"  data-aos-duration="1000">
      <div class="detail-content">
        <div v-for="content in article?.content" :key="content">
          <img v-if="content?.includes('https://')" :src="content" />
          <p v-else>{{ content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import 'aos/dist/aos.css'
import AOS from 'aos'

import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute();
const router = useRouter();
const articles = JSON.parse(localStorage.getItem('articles'))// 전체 기사 리스트 
const article = ref() // id 로 매핑된 리스트

// 전체 리스트 중 id 맞는 리스트 걸러내기
function loadArticle() {
  for (let list of articles) {
    if (list.id == route.params.id) {
      article.value = list;  
      break;  
    }
  }

  if (!article.value) {
    router.push('/')
  }
}

function goBack() {
  router.go(-1);
}


onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  loadArticle();
  AOS.init();
  AOS.refresh();
})
</script>

<style>
@import '@/assets/scss/page/detail.scss';
</style>