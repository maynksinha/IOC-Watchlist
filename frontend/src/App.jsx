import { lazy, useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { fetchTags } from './store/tagSlice'
import FilterBar from './components/FilterBar'
import withSuspense from './utils/withSuspense'
import CircularLoader from './utils/Loader'

const AddIOCForm = withSuspense(lazy(() => import('./components/AddIOCForm')))
const IOCTable   = withSuspense(
  lazy(() => import('./components/IOCTable')),
  <CircularLoader size="lg" />
)

export default function App() {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(fetchTags())
  }, [dispatch])

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <h1 className="text-xl font-semibold text-gray-800 mb-6">IOC Watchlist</h1>
      <AddIOCForm />
      <FilterBar />
      <IOCTable />
    </div>
  )
}
