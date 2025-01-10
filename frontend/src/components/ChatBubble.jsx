function ChatBubble({ text, sender }) {
    return (
      <div className={`p-3 rounded-lg max-w-md mb-2 ${sender === "user" ? "bg-blue-500 text-white ml-auto" : "bg-gray-200 text-black"}`}>
        <p>{text}</p>
      </div>
    );
  }
  
  export default ChatBubble;