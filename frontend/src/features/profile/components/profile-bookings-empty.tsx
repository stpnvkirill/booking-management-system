export default function CardEmpty() {
  return (
    <div className="skeleton-striped flex w-full items-center justify-center min-h-[calc(100vh-350px)] border-none rounded-box border p-4 overflow-y-auto">
      <p className="text-center text-neutral mt-1 mb-1">
        У вас нет активных бронирований.
      </p>
    </div>
  );
}
