import API from './api';

// 📌 Iniciar Fine-Tuning
export const startFineTune = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await API.post("/fine-tune/start", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
};

// 📌 Verificar Estado
export const getFineTuneStatus = async (fineTuneId) => {
    const response = await API.get(`/fine-tune/status/${fineTuneId}`);
    return response.data;
};