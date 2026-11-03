import { Suspense } from 'react'
import CircularLoader from './Loader'

export default function withSuspense(Component, fallback = <CircularLoader />) {
  return function SuspenseWrapper(props) {
    return (
      <Suspense fallback={fallback}>
        <Component {...props} />
      </Suspense>
    )
  }
}
