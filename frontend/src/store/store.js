import { configureStore } from '@reduxjs/toolkit'
import iocReducer    from './iocSlice'
import tagReducer    from './tagSlice'
import filterReducer from './filterSlice'

export const store = configureStore({
  reducer: {
    iocs:   iocReducer,
    tags:   tagReducer,
    filter: filterReducer,
  },
})
