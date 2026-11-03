import { createAsyncThunk } from '@reduxjs/toolkit'

export function createApiThunk(typePrefix, apiFn) {
  return createAsyncThunk(typePrefix, async (arg, { rejectWithValue }) => {
    try {
      const res = await apiFn(arg)
      // API always returns { success, message, error_code, data }
      return res.data.data
    } catch (err) {
      const body = err.response?.data ?? {}
      return rejectWithValue({
        status:     err.response?.status,
        message:    body.message  ?? err.message,
        error_code: body.error_code ?? 'UNKNOWN_ERROR',
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
