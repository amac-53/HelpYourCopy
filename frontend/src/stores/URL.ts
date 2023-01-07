import { defineStore } from 'pinia';

export const useStoreURL = defineStore('URL', () => {
    const URL = "http://127.0.0.1";
    const ports = "8081";

    // getters
    const getURL = () => {
        return URL + ":" + ports + '/';
    }

    return { 
        getURL
    };
});