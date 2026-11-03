import apiClient from './apiClient'
import { API_ROUTES } from './routes.enum'

export const fetchIOCsAPI = (params) => apiClient.get(API_ROUTES.IOCS, { params })
export const createIOCAPI = (data)   => apiClient.post(API_ROUTES.IOCS, data)
export const deleteIOCAPI = (id)     => apiClient.delete(API_ROUTES.IOC_BY_ID(id))
