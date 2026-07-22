export default function Pagination({ page, hasNext, onPrevious, onNext }) {
  return (
    <div className="flex justify-between items-center mt-6">
      <button
        onClick={onPrevious}
        disabled={page === 0}
        className="px-4 py-2 rounded bg-slate-900 text-white disabled:bg-gray-300"
      >
        ← Previous
      </button>

      <span className="font-medium">Page {page + 1}</span>

      <button
        onClick={onNext}
        disabled={!hasNext}
        className="px-4 py-2 rounded bg-slate-900 text-white disabled:bg-gray-300"
      >
        Next →
      </button>
    </div>
  );
}
