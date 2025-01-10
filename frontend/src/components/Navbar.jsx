import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { token, logout } = useAuth();

  return (
    <nav className="bg-blue-600 text-white py-4 px-6 shadow-md">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Chatbot Pymes</h1>
        <ul className="flex space-x-4">
          <li><Link to="/" className="hover:underline">Inicio</Link></li>
          {token ? (
            <>
              <li><Link to="/chat" className="hover:underline">Chat</Link></li>
              <li><Link to="/documents" className="hover:underline">Documentos</Link></li>
              <li><Link to={"/finetune"} className="hover:underline">FineTune</Link></li>
              <li>
                <button onClick={logout} className="hover:underline">Cerrar Sesión</button>
              </li>
            </>
          ) : (
            <li><Link to="/login" className="hover:underline">Iniciar Sesión</Link></li>
          )}
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;