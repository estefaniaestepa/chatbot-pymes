import { useState } from "react";
import API from "../services/api";
import ChatBubble from "../components/ChatBubble";
import Input from "../components/Input";
import Button from "../components/Button";
import Loader from "../components/Loader";

function ChatPage() {
  const [message, setMessage] = useState("");
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    try {
      const response = await API.post("/chat/message", { message });
      setResponses([
        ...responses,
        { sender: "user", text: message },
        { sender: "bot", text: response.data.bot_response },
      ]);
      setMessage("");
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto mt-12 p-6 bg-gradient-to-r from-blue-50 to-white shadow-lg rounded-lg">
      <h2 className="text-3xl font-extrabold text-gray-800 mb-6 text-center">
        Chat con Asistente
      </h2>
      <div className="h-72 overflow-y-auto mb-6 border border-gray-300 p-4 rounded-lg bg-gray-50">
        {responses.map((res, index) => (
          <ChatBubble key={index} text={res.text} sender={res.sender} />
        ))}
        {loading && <Loader />}
      </div>
      <div className="flex gap-4">
        <Input
          type="text"
          placeholder="Escribe tu mensaje..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <Button
          text="Enviar"
          onClick={sendMessage}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold transition duration-300 ease-in-out"
        />
      </div>
    </div>
  );
}

export default ChatPage;
