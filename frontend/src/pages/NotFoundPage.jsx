function NotFoundPage() {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-100 to-gray-200">
      <h1 className="text-8xl font-extrabold text-red-600 drop-shadow-lg">
        404
      </h1>
      <p className="text-lg text-gray-700 mt-4 text-center">
        Lo sentimos, la página que buscas no existe.
      </p>
      <a
        href="/"
        className="mt-8 px-6 py-3 bg-blue-600 text-white text-lg rounded-lg shadow-md hover:bg-blue-700 hover:shadow-lg transition-all duration-300"
      >
        Volver al Inicio
      </a>
    </div>
  );
}

export default NotFoundPage;
