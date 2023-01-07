import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useStoreFile = defineStore('file', () => {
    const name = ref('');
    return { name };
});