import React from 'react';
import useBookings from '../hooks/useBookings';

export const BookingsList: React.FC = () => {
  const { data, loading, error, refetch } = useBookings();

  if (loading) return <div>Loading bookings...</div>;
  if (error)
    return (
      <div>
        Error loading bookings: {String(error.message)}
        <br />
        <button onClick={refetch}> Retry </button>
      </div>
    );
  console.log(data);
  console.log(data?.length);
  if (!data || data.length === 0) return <div>No bookings found.</div>;
  console.log(data);
  return (
    <div>
      <h3>Bookings</h3>
      <ul>
        {data.map((b) => (
          <li key={b.id}>
            {b.id} — {b.resourceId ?? '-'} — {b.startAt ?? '-'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BookingsList;
