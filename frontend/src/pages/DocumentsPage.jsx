import { useEffect, useState } from "react";
import API from "../services/api";
import Loader from "../components/Loader";

function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await API.get("/documents/all");
      setDocuments(response.data.documents || []);
    } catch (error) {
      console.error("Error al obtener documentos:", error);
      setError("Error al obtener documentos. Intenta de nuevo más tarde.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-12 p-8 bg-gradient-to-b from-gray-50 to-white shadow-lg rounded-lg">
      <h2 className="text-3xl font-extrabold text-gray-800 mb-6 text-center">
        Documentos
      </h2>
      <ul className="divide-y divide-gray-300">
        {documents.map((doc) => (
          <li
            key={doc.file_name}
            className="py-4 px-6 bg-gray-100 rounded-lg shadow-sm mb-4 hover:shadow-md transition-shadow duration-300"
          >
            <p className="text-lg font-semibold text-gray-700">
              <strong>Nombre:</strong> {doc.file_name}
            </p>
            <p className="text-sm text-gray-600">
              <strong>Subido por:</strong> {doc.uploaded_by}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DocumentsPage;
