import Button from '@/shared/components/button/button';
import { firstBigLetter } from '@/shared/types/functions';
import type { ResourceItem } from '@/shared/types/types';

export interface CardProps {
  data: ResourceItem | undefined;
  activeTab: Tabs;
  setActiveTab: React.Dispatch<React.SetStateAction<Tabs>>;
  handleResourceClick: (data: ResourceItem | undefined) => void;
}
import type { Tabs } from '@/shared/types/types';
export default function BookingCard({ handleResourceClick, data }: CardProps) {
  return (
    <div className="bg-base-200 p-5 mb-4 rounded-2xl hover:bg-base-100 duration-200">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-semibold mb-1 text-accent-content">
            {data?.name}
          </h3>
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-accent rounded-2xl text-base-content pt-0.5 pb-0.5 pr-2 pl-2 text-sm font-medium">
              {firstBigLetter(data?.resource_type)}
            </span>
            <span className="text-accent-content text-sm">•</span>
            <span className="text-accent-content text-sm">
              {/* {data?.start_time && data.end_time
                ? `${getDDMMDateFromUTCString(data.start_time)} - ${getDDMMDateFromUTCString(data.end_time)}`
                : 'Даты не указаны'} */}
              {data?.description}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span>{data?.location}</span>
            {/* <span className="text-amber-400">★ {data?.rating}</span> */}
            {/* {data?.timeLeft && (
              <span className="text-accent-content text-sm">
                🔽 {data?.timeLeft}
              </span>
            )} */}
          </div>
        </div>
        <div className="text-right">
          <div className="text-xl font-bold mb-2">
            {data?.price_per_hour ? data.price_per_hour.toLocaleString() : '0'} ₽
          </div>
          <div className="flex flex-col gap-2">
            <Button
              label="Подробнее"
              onClick={() => {
                // console.log(data);
                if (data) handleResourceClick?.(data);
              }}
              size="sm"
              variant="primary"
              width="responsive"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
