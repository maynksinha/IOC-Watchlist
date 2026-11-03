import { lazy, useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { fetchTags } from './store/tagSlice'
import FilterBar from './components/FilterBar'
import withSuspense from './utils/withSuspense'
import CircularLoader from './utils/Loader'
import { theme } from './theme/theme'

const AddIOCForm = withSuspense(lazy(() => import('./components/AddIOCForm')))
const IOCTable   = withSuspense(
  lazy(() => import('./components/IOCTable')),
  <CircularLoader size="lg" />,
)

export default function App() {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(fetchTags())
  }, [dispatch])

  return (
    <div className="min-h-screen">
      <header className={theme.header.bar}>
        <div className={theme.header.inner}>
          <span className={theme.header.logo}>🛡</span>
          <div>
            <h1 className={theme.header.title}>IOC Watchlist</h1>
            <p className={theme.header.subtitle}>Ingest, normalize, tag and track indicators of compromise</p>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6 flex flex-col gap-5">
        <AddIOCForm />
        <FilterBar />
        <IOCTable />
      </main>
    </div>
  )
}
