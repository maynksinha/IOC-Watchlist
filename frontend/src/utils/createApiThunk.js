import { createAsyncThunk } from '@reduxjs/toolkit'

export function createApiThunk(typePrefix, apiFn) {
  return createAsyncThunk(typePrefix, async (arg, { rejectWithValue }) => {
    try {
      const res = await apiFn(arg)
      return res.data
    } catch (err) {
      return rejectWithValue({
        status: err.response?.status,
        data:   err.response?.data ?? { detail: err.message },
      })
    }
  })
}

export function addApiCases(builder, thunk, onFulfilled) {
  builder
    .addCase(thunk.pending, (state) => {
      state.isLoading = true
      state.error = null
    })
    .addCase(thunk.fulfilled, (state, action) => {
      state.isLoading = false
      onFulfilled(state, action)
    })
    .addCase(thunk.rejected, (state, action) => {
      state.isLoading = false
      state.error = action.payload
    })
}
