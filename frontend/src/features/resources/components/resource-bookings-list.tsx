import type { ResourceItem, ResourceTabs } from '@/shared/types/types';
import { AnimatePresence, motion } from 'framer-motion';
import BookingCard from './resources-card';
interface BookingsListProps {
  data: ResourceItem[]; // Ожидаем уже отфильтрованный массив
  setResourceActiveTab: React.Dispatch<React.SetStateAction<ResourceTabs>>;
  activeResourceTab: ResourceTabs | undefined;
  handleResourceClick: (data: ResourceItem | undefined) => void;
}
export default function BookingList({
  data,
  activeResourceTab,
  setResourceActiveTab,
  handleResourceClick,
}: BookingsListProps) {
  console.log(data);
  if (data.length === 0) {
    return (
      <p className="text-center mt-4 text-accent">Бронирования не найдены.</p>
    );
  }
  return (
    <div className="flex flex-col gap-4 max-h-[calc(100vh-310px)] overflow-y-scroll">
      <AnimatePresence mode="popLayout">
        {data.map((ResourceItem) => (
          <motion.div
            key={ResourceItem.id}
            layout
            initial={{ opacity: 0, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <BookingCard
              data={ResourceItem}
              activeResourceTab={activeResourceTab}
              setResourceActiveTab={setResourceActiveTab}
              handleResourceClick={handleResourceClick}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
