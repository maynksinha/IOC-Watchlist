import apiClient from './apiClient'
import { API_ROUTES } from './routes.enum'

export const fetchTagsAPI = () => apiClient.get(API_ROUTES.TAGS)
