import { useEffect, useState } from 'react';
// import Button from "@/shared/components/button/button";
import Header from './components/resources-header';
import List from './components/resources-list';
import { Spinner } from '@/shared/components/spinner/spinner';
import axios from 'axios';
import ErrMessage from './components/resource-error';
import type { BookingItem } from '@/shared/types/types';
import type { Filters } from '@/shared/types/types';
import FilterBTNS from './components/resources-filters';
import BookingList from './components/resource-bookings-list';

export default function ResourcesScreen() {
  const [activeFilter, setActiveFilter] = useState<Filters | undefined>('Все');
  const BookingItems: BookingItem[] = [];
  const [data, setData] = useState<BookingItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<BookingItem[]>(
          'http://localhost:88/api/bookings/all/',
          {
            headers: {
              Accept: 'application/json',
              Authorization: 'Bearer ' + import.meta.env.VITE_BEARER_TOKEN,
            },
          }
        );
        setData(response?.data);
      } catch (err) {
        setError('Error fetching data. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);
  BookingItems.push(data);
  console.log(data);
  console.log(BookingItems.length);
  console.log(BookingItems);

  const filteredBookings = BookingItems.filter((booking: BookingItem) => {
    if (activeFilter === 'Все') {
      return true;
    }
    return booking?.booking_type?.toLowerCase() === activeFilter?.toLowerCase();
  });
  return (
    <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans">
      <div className="p-4">
        {/* Заголовок */}
        <Header title="NightBooks" />
        {/* Фильтры */}
        <FilterBTNS
          activeFilter={activeFilter}
          setActiveFilter={setActiveFilter}
        />
        {/* Список бронирований */}
        <List count={filteredBookings.length} />
        {/* Карточки ресурсов */}
        {error ? <ErrMessage /> : ''}
        {loading ? (
          <Spinner />
        ) : data.length != 0 ? (
          <BookingList data={filteredBookings} />
        ) : (
          ''
        )}
      </div>
    </div>
  );
}
