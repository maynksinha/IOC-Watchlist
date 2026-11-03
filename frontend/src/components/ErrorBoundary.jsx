import { Component } from 'react'
import { theme } from '../theme/theme'

export default class ErrorBoundary extends Component {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error, info) {
    // eslint-disable-next-line no-console
    console.error('UI crashed:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="max-w-md mx-auto mt-24 text-center">
          <div className={theme.card}>
            <h2 className="text-lg font-semibold text-slate-800 mb-2">Something went wrong</h2>
            <p className="text-sm text-slate-500 mb-4">
              The interface hit an unexpected error. Reloading usually fixes it.
            </p>
            <button onClick={() => window.location.reload()} className={theme.button.primary}>
              Reload page
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
