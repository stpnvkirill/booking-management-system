import FilterBTNS from './resources-filters';
import BookingList from './resource-bookings-list';
import ErrMessage from '../../../shared/components/messages/error-message';
import Header from '../../../shared/components/header/header';
import List from './resources-list';
import { Spinner } from '@/shared/components/spinner/spinner';
import type { ResourceItem, Filters } from '@/shared/types/types';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Message from '@/shared/components/messages/message';
type Tabs = 'main' | 'details';
interface ResourceMainProps {
  activeTab: Tabs;
  setActiveTab: React.Dispatch<React.SetStateAction<Tabs>>;
  handleResourceClick: (data: ResourceItem | undefined) => void;
}

export default function ResourceMain({
  activeTab,
  setActiveTab,
  handleResourceClick,
}: ResourceMainProps) {
  const [activeFilter, setActiveFilter] = useState<Filters | undefined>('Все');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ResourceItem[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<ResourceItem[]>(
          `${import.meta.env.VITE_SERVER_IP}/api/resources/all`,
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
  // uv run python -c "from app.api.security import compress_token; print(compress_token('019bfe4f-701f-78c8-9914-886ec5877e6b'))"
  const filteredBookings = data.filter((booking: ResourceItem) => {
    if (activeFilter === 'Все') {
      return true;
    }
    return booking?.resource_type?.toLowerCase() === activeFilter?.toLowerCase();
  });
  return (
    <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans">
      <div className="p-4">
        {/* Заголовок */}
        <Header title="NightBooks" subtitle="Ресурсы" />
        {/* Фильтры */}
        <FilterBTNS
          activeFilter={activeFilter}
          setActiveFilter={setActiveFilter}
        />
        {/* Список бронирований */}
        <List count={filteredBookings.length} />
        {/* Карточки ресурсов */}
        {error ? <ErrMessage error={error} /> : data.length == 0 && !loading ? <Message message="Нет доступных бронирований"/> : ''}
        {loading ? (
          <Spinner />
        ) : data.length != 0 ? (
          <BookingList
            handleResourceClick={handleResourceClick}
            data={filteredBookings}
            activeTab={activeTab}
            setActiveTab={setActiveTab}
          />
        ) : ""}
      </div>
    </div>
  );
}
