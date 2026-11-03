export const theme = {
  badge: {
    url:    'bg-blue-50 text-blue-700 ring-1 ring-blue-200',
    ipv4:   'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200',
    domain: 'bg-teal-50 text-teal-700 ring-1 ring-teal-200',
    md5:    'bg-slate-100 text-slate-600 ring-1 ring-slate-200',
    sha1:   'bg-slate-100 text-slate-600 ring-1 ring-slate-200',
    sha256: 'bg-slate-100 text-slate-600 ring-1 ring-slate-200',
    default:'bg-slate-100 text-slate-600 ring-1 ring-slate-200',
  },

  button: {
    primary:     'inline-flex items-center justify-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg shadow-sm hover:bg-indigo-700 active:bg-indigo-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors',
    secondary:   'inline-flex items-center justify-center px-4 py-2 bg-white text-slate-700 text-sm font-medium rounded-lg border border-slate-300 hover:bg-slate-50 disabled:opacity-50 transition-colors',
    danger:      'text-red-500 hover:text-red-700 text-xs font-medium transition-colors',
    dangerSolid: 'inline-flex items-center justify-center px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg shadow-sm hover:bg-red-700 active:bg-red-800 disabled:opacity-50 transition-colors',
    ghost:       'text-slate-400 hover:text-slate-700 transition-colors',
  },

  input: {
    base:     'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm bg-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition',
    textarea: 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm font-mono bg-white resize-none placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition',
    chip:     'flex flex-wrap items-center gap-1.5 border border-slate-300 rounded-lg px-2 py-1.5 min-h-[40px] bg-white focus-within:ring-2 focus-within:ring-indigo-400 focus-within:border-indigo-400 transition',
    error:    'border-red-400 focus:ring-red-400 focus:border-red-400',
  },

  card: 'bg-white border border-slate-200 rounded-xl p-5 shadow-sm',

  alert: {
    warning: 'bg-amber-50 border border-amber-200 rounded-lg p-3 text-sm text-amber-800',
    error:   'text-red-600 text-sm',
    success: 'text-emerald-600 text-sm',
  },

  tag: {
    chip:      'inline-flex items-center bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded-md',
    inputChip: 'inline-flex items-center gap-1 bg-indigo-50 text-indigo-700 text-xs font-medium px-2 py-0.5 rounded-md ring-1 ring-indigo-200',
  },

  combobox: {
    control:      'flex flex-wrap items-center gap-1.5 border border-slate-300 rounded-lg px-2 py-1.5 min-h-[40px] bg-white cursor-text focus-within:ring-2 focus-within:ring-indigo-400 focus-within:border-indigo-400 transition',
    menu:         'absolute z-20 mt-1 w-full max-h-56 overflow-auto bg-white border border-slate-200 rounded-lg shadow-lg py-1 text-sm animate-fade-in',
    option:       'px-3 py-2 cursor-pointer text-slate-700',
    optionActive: 'bg-indigo-50 text-indigo-700',
  },

  table: {
    wrapper: 'overflow-x-auto border border-slate-200 rounded-xl bg-white shadow-sm',
    header:  'bg-slate-50 text-slate-500 text-xs uppercase tracking-wide',
    row:     'border-t border-slate-100 hover:bg-slate-50/70 transition-colors',
    cell:    'px-4 py-3',
  },

  text: {
    muted:   'text-slate-400',
    subtle:  'text-slate-500',
    label:   'text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3',
    section: 'text-xl font-semibold text-slate-800',
  },

  filter: {
    bar:    'flex flex-wrap items-center gap-3 bg-white border border-slate-200 rounded-xl px-4 py-3 shadow-sm text-sm',
    select: 'border border-slate-300 rounded-lg px-3 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition',
  },

  header: {
    bar:      'border-b border-slate-200 bg-white',
    inner:    'max-w-5xl mx-auto px-4 py-4 flex items-center gap-3',
    title:    'text-lg font-semibold text-slate-800',
    subtitle: 'text-xs text-slate-400',
    logo:     'flex items-center justify-center h-9 w-9 rounded-lg bg-indigo-600 text-white text-lg',
  },

  toast: {
    viewport: 'fixed bottom-4 right-4 z-50 flex flex-col gap-2 w-80 max-w-[calc(100vw-2rem)]',
    base:     'flex items-start gap-2 px-4 py-3 rounded-lg shadow-lg text-sm text-white animate-toast-in',
    success:  'bg-emerald-600',
    error:    'bg-red-600',
    info:     'bg-slate-700',
  },

  dialog: {
    overlay: 'fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in',
    panel:   'bg-white rounded-xl shadow-xl w-full max-w-sm p-5 animate-dialog-in',
    title:   'text-base font-semibold text-slate-800',
    message: 'text-sm text-slate-500 mt-1.5',
    actions: 'flex justify-end gap-2 mt-5',
  },
}
