/**
 * Servicio de carga de archivos
 */

import apiClient from './client'

export const uploadService = {
  async uploadStock(file) {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post('/upload/stock', formData)
    return response.data
  },
}
