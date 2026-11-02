/**
 * Servicio de carga de archivos
 */

import apiClient from './client'

export const uploadService = {
  /**
   * Carga un archivo CSV
   */
  async uploadCSV(file, entity) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('entity', entity)

    const response = await apiClient.post('/upload/csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}
