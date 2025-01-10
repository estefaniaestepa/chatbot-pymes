import { useState } from "react";
import { startFineTune, getFineTuneStatus } from "../services/fineTune";
import Loader from "../components/Loader";
import Button from "../components/Button";

function FineTunePage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [fineTuneId, setFineTuneId] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError("");
    setStatus("");
  };

  const handleStartFineTune = async () => {
    if (!file) {
      setError("Por favor selecciona un archivo JSONL.");
      return;
    }

    setLoading(true);
    setError("");
    setStatus("");

    try {
      const response = await startFineTune(file);
      setFineTuneId(response.fine_tune_id);
      setStatus("¡El proceso de Fine-Tuning se ha iniciado correctamente!");
    } catch (err) {
      setError(`Error al iniciar el proceso de Fine-Tuning: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckStatus = async () => {
    if (!fineTuneId) {
      setError("No hay un ID de Fine-Tune para verificar.");
      return;
    }

    setLoading(true);
    setError("");
    setStatus("");

    try {
      const response = await getFineTuneStatus(fineTuneId);
      setStatus(`Estado actual: ${response.status}`);
    } catch (err) {
      setError("Error al verificar el estado del Fine-Tuning.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 p-6 bg-white shadow-md rounded-md">
      <h2 className="text-2xl font-bold mb-4 text-center">Fine-Tuning del Modelo</h2>
      <input type="file" accept=".jsonl" onChange={handleFileChange} className="w-full p-2 border rounded-md mb-4" />
      <Button text="Iniciar Fine-Tuning" onClick={handleStartFineTune} className="w-full mb-2" />
      <Button text="Verificar Estado" onClick={handleCheckStatus} className="w-full" />
      {loading && <Loader />}
      {status && <p className="mt-4 text-green-600 text-center">{status}</p>}
      {error && <p className="mt-4 text-red-600 text-center">{error}</p>}
    </div>
  );
}

export default FineTunePage;