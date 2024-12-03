import axios from "axios";

const API_URL = "http://localhost:49529";

export const sendChatbotQuery = async (text, image) => {
    const formData = new FormData();
    formData.append("symptoms", text);
    if (image) formData.append("image", image);
  
    try {
      const response = await axios.post(`${API_URL}/prompt`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error sending chatbot query:", error);
      throw error;
    }
  };