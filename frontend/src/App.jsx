import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import AppRoutes from "./routes/AppRoutes";

function App() {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col justify-between">
      {/* Barra de navegación */}
      <Navbar />

      {/* Contenido principal */}
      <main className="flex-grow">
        <AppRoutes />
      </main>

      {/* Pie de página */}
      <Footer />
    </div>
  );
}

export default App;