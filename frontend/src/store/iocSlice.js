import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { fetchIOCsAPI, deleteIOCAPI } from '../services/iocService'
import { fetchTags } from './tagSlice'
import { createApiThunk, addApiCases } from '../utils/createApiThunk'

export const fetchIOCs = createApiThunk('iocs/fetchAll', fetchIOCsAPI)

export const deleteIOC = createAsyncThunk(
  'iocs/delete',
  async (id, { dispatch, getState, rejectWithValue }) => {
    try {
      await deleteIOCAPI(id)
      const { typeFilter, tagFilter } = getState().filter
      dispatch(fetchIOCs({ type: typeFilter || undefined, tag: tagFilter || undefined }))
      dispatch(fetchTags())
      return id
    } catch (err) {
      return rejectWithValue({
        status: err.response?.status,
        data:   err.response?.data ?? { detail: err.message },
      })
    }
  }
)

const iocSlice = createSlice({
  name: 'iocs',
  initialState: {
    items:     [],
    total:     0,
    page:      1,
    isLoading: false,
    error:     null,
  },
  reducers: {},
  extraReducers: (builder) => {
    addApiCases(builder, fetchIOCs, (state, action) => {
      state.items = action.payload.items
      state.total = action.payload.total
      state.page  = action.payload.page
    })
    builder
      .addCase(deleteIOC.pending,   (state) => { state.isLoading = true })
      .addCase(deleteIOC.fulfilled, (state) => { state.isLoading = false })
      .addCase(deleteIOC.rejected,  (state, action) => {
        state.isLoading = false
        state.error = action.payload
      })
  },
})

export default iocSlice.reducer
