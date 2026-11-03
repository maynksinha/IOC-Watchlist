export const theme = {
  badge: {
    url:    'bg-blue-100 text-blue-800',
    ipv4:   'bg-green-100 text-green-800',
    domain: 'bg-teal-100 text-teal-800',
    md5:    'bg-gray-100 text-gray-700',
    sha1:   'bg-gray-100 text-gray-700',
    sha256: 'bg-gray-100 text-gray-700',
    default:'bg-gray-100 text-gray-700',
  },

  button: {
    primary: 'px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:opacity-50',
    danger:  'text-red-400 hover:text-red-600 text-xs',
    ghost:   'text-gray-500 hover:text-gray-800',
  },

  input: {
    base:     'border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400',
    textarea: 'border border-gray-300 rounded px-3 py-2 text-sm font-mono resize-none focus:outline-none focus:ring-1 focus:ring-blue-400',
    chip:     'flex flex-wrap gap-1 border border-gray-300 rounded px-2 py-1 min-h-[36px] focus-within:ring-1 focus-within:ring-blue-400',
  },

  card: 'bg-white border border-gray-200 rounded p-4',

  alert: {
    warning: 'bg-yellow-50 border border-yellow-300 rounded p-3 text-sm text-yellow-800',
    error:   'text-red-600 text-sm',
  },

  tag: {
    chip:      'bg-gray-100 text-gray-600 text-xs px-1.5 py-0.5 rounded',
    inputChip: 'flex items-center gap-1 bg-gray-200 text-gray-700 text-xs px-2 py-0.5 rounded',
  },

  table: {
    wrapper: 'overflow-x-auto border border-gray-200 rounded',
    header:  'bg-gray-50 text-gray-600 text-xs uppercase',
    row:     'border-b border-gray-100 hover:bg-gray-50',
    cell:    'px-3 py-2',
  },

  text: {
    muted:   'text-gray-400',
    subtle:  'text-gray-500',
    label:   'text-sm font-semibold text-gray-600 uppercase tracking-wide mb-3',
    section: 'text-xl font-semibold text-gray-800 mb-6',
  },

  filter: {
    bar:    'flex items-center gap-3 bg-gray-50 border border-gray-200 rounded px-4 py-2 mb-4 text-sm',
    select: 'border border-gray-300 rounded px-2 py-1',
  },
}
