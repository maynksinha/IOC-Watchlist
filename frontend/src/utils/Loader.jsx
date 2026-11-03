const SIZES = { sm: 'h-4 w-4', md: 'h-8 w-8', lg: 'h-12 w-12' }

export default function CircularLoader({ size = 'md' }) {
  return (
    <div className="flex justify-center items-center p-6">
      <div
        className={`${SIZES[size]} animate-spin rounded-full border-2 border-gray-200 border-t-blue-600`}
        role="status"
        aria-label="Loading"
      />
    </div>
  )
}
