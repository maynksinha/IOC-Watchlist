import { createSlice } from '@reduxjs/toolkit'
import { fetchTagsAPI } from '../services/tagService'
import { createApiThunk, addApiCases } from '../utils/createApiThunk'

export const fetchTags = createApiThunk('tags/fetchAll', fetchTagsAPI)

const tagSlice = createSlice({
  name: 'tags',
  initialState: { items: [], isLoading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    addApiCases(builder, fetchTags, (state, action) => {
      state.items = action.payload
    })
  },
})

export default tagSlice.reducer
