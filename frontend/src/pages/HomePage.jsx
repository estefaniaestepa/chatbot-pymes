function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-b from-blue-50 to-gray-50">
      <h1 className="text-5xl font-extrabold text-blue-700 drop-shadow-lg">
        ¡Bienvenido al Sistema!
      </h1>
      <p className="text-lg text-gray-700 mt-4 text-center max-w-lg">
        Explora las diferentes funcionalidades desde el menú principal.
      </p>
      <a
        href="/login"
        className="mt-8 px-6 py-3 bg-blue-600 text-white text-lg rounded-lg shadow-md hover:bg-blue-700 hover:shadow-lg transition-all duration-300"
      >
        Iniciar Sesión
      </a>
    </div>
  );
}

export default HomePage;
