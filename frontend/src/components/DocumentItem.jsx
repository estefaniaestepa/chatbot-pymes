function DocumentItem({ name, uploadedBy, uploadedAt }) {
    return (
      <div className="p-4 border-b flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold">{name}</h3>
          <p className="text-sm text-gray-500">Subido por: {uploadedBy}</p>
          <p className="text-sm text-gray-500">Fecha: {new Date(uploadedAt).toLocaleDateString()}</p>
        </div>
        <button className="bg-red-500 text-white px-2 py-1 rounded-md hover:bg-red-600">
          Eliminar
        </button>
      </div>
    );
  }
  
  export default DocumentItem;