import { createSlice } from '@reduxjs/toolkit'

const filterSlice = createSlice({
  name: 'filter',
  initialState: { typeFilter: '', tagFilter: '' },
  reducers: {
    setTypeFilter: (state, action) => { state.typeFilter = action.payload },
    setTagFilter: (state, action) => { state.tagFilter = action.payload },
    clearFilters: (state) => { state.typeFilter = ''; state.tagFilter = '' },
  },
})

export const { setTypeFilter, setTagFilter, clearFilters } = filterSlice.actions
export default filterSlice.reducer
