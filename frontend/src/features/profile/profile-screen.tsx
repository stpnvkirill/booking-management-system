import { AnimatePresence, motion } from 'framer-motion';
import ActiveBookingCard from './components/profile-card.tsx';
import CardEmpty from './components/profile-bookings-empty.tsx';
import type { BookingItem, } from '@/shared/types/types.tsx';
import ProfileSettings from './components/profile-user-settings.tsx';
import axios from 'axios';
import { useState } from 'react';
import { Spinner } from '@/shared/components/spinner/spinner.tsx';
import ErrMessage from '@/shared/components/messages/error-message.tsx';


export default function ProfileScreen() {
  // const [resources, setResources] = useState<ResourceItem[]>()
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<BookingItem[] | undefined>();
  const fetchData = async () => {
    try {
      const response = await axios.get<BookingItem[]>(
        `${import.meta.env.VITE_SERVER_IP}/api/bookings/all`,
        {
          headers: {
            Accept: 'application/json',
            Authorization: 'Bearer ' + import.meta.env.VITE_BEARER_TOKEN,
          },
        }
      );
      // console.log(response.data)
      const ResourcesFilteredByDate = response.data.filter(booking => booking.user_id == import.meta.env.VITE_APP_USER_ID);
      // console.log(ResourcesFilteredByDate);
      setData(ResourcesFilteredByDate)
    } catch (err) {
      setError('Error fetching data. Please try again later.');
      console.error(err, error)
    } finally {
      setLoading(false);
    }
  };
  fetchData()
  return (
    <>
      {/* Настройки */}
      <ProfileSettings />

      {
        loading ? <Spinner /> :
          error ? <ErrMessage error={error} /> :
            data?.length === 0 ? <CardEmpty /> :
              data?.length != 0 && data != undefined ? (
                <div className="flex-1 overflow-y-auto pb-24 touch-pan-y scrollbar-hide max-h-[calc(100vh-280px)]">
                  {/* Список активных карточек */}
                  <div className="flex flex-col gap-4">
                    <AnimatePresence>
                      {data?.map((booking) => (
                        <motion.div
                          key={booking?.id}
                          initial={{ opacity: 1, height: 'auto' }}
                          exit={{
                            opacity: 0,
                            height: 0,
                            marginBottom: 0,
                            overflow: 'hidden',
                          }}
                          transition={{ duration: 0.3 }}
                        >
                          <ActiveBookingCard
                            data={booking}
                            onCancel={() => {
                              // handleCancelBooking(booking.id!)
                            }}
                          />
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </div>
                </div>
              ) : ""
      }
    </>
  );
}
