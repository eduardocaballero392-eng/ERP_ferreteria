/**
 * Servicio de carga de archivos
 */

import apiClient from './client'

export const uploadService = {
  async uploadStock(file) {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post('/upload/stock', formData, {
      // La API necesita multipart/form-data (con su boundary) para recibir el archivo.
      // El cliente global usa JSON por defecto, así que aquí reemplazamos ese encabezado.
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
}
