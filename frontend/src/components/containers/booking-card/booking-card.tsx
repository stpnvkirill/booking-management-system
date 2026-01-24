import { type PropsWithChildren } from 'react';
import Button from '../../small/button/button';
import { useBookingContext } from '../bookingContext/bookingContext.tsx';
import type { BookingItem } from '../bookingContext/bookingContext.tsx';

interface CardProps {
  data?: BookingItem;
  key?: string | number;
}

export const BookingCard = ({
  data,
}: PropsWithChildren<CardProps>): React.ReactElement => {
  const {

    handleResourceClick = (item?: BookingItem) => {
      if (!item) {
        return;
      }
    },
  } = useBookingContext();
  return (
    <div className="bg-base-200 p-5 mb-4 rounded-2xl hover:bg-base-100 duration-200">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-semibold mb-1 text-accent-content">
            {data?.title}
          </h3>
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-accent rounded-2xl text-base-content pt-0.5 pb-0.5 pr-2 pl-2 text-sm font-medium">
              {data?.type}
            </span>
            <span className="text-accent-content text-sm">•</span>
            <span className="text-accent-content text-sm">
              {data?.capacity}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-base-content text-sm">
              📌 {data?.location}
            </span>
            <span className="text-amber-400">★ {data?.rating}</span>
            {data?.timeLeft && (
              <span className="text-accent-content text-sm">
                🔽 {data?.timeLeft}
              </span>
            )}
          </div>
        </div>
        <div className="text-right">
          <div className="text-xl font-bold mb-2">
            {data?.price ? data.price.toLocaleString() : '0'} ₽
          </div>
          <div className="flex flex-col gap-2">
            <Button
              label="Открыть"
              onClick={() => {
                if (data) handleResourceClick(data);
              }}
              size="sm"
              variant="primary"
              width="responsive"
            />
            {/* <Button
              label="Бронь"
              onClick={() => {
                handleConfirmBooking();
              }}
              variant="info"
              width="responsive"
              size="sm"
            /> */}
          </div>
        </div>
      </div>
    </div>
  );
};
