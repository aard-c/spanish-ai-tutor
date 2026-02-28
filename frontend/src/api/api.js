import axios from 'axios';

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
})

export const  sendSentence = async (sentence) => {
    const response = await api.post("/chat/correct", {sentence});
    return response.data;
}

export const getHistory = async () => {
    const response = await api.get("/chat/history");
    return response.data;
}