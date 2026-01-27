import { useEffect, useState, useCallback } from 'react';
import { getAllBookings } from '../API/bookings';
import type { Booking } from '../types/api/get-all-bookings';

export function useBookings() {
  const [data, setData] = useState<Booking[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const bookings = await getAllBookings();
      setData(bookings);
    } catch (err: unknown) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { data, loading, error, refetch: fetch } as const;
}

export default useBookings;
