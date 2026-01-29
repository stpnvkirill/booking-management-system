import type { ResourceItem } from '@/shared/types/types';
import { AnimatePresence, motion } from 'framer-motion';
import BookingCard from './resources-card';
type Tabs = 'main' | 'details';
interface BookingsListProps {
  data: ResourceItem[]; // Ожидаем уже отфильтрованный массив
  activeTab: Tabs;
  setActiveTab: React.Dispatch<React.SetStateAction<Tabs>>;
  handleResourceClick: (data: ResourceItem | undefined) => void;
}
export default function BookingList({
  data,
  activeTab,
  setActiveTab,
  handleResourceClick,
}: BookingsListProps) {
  console.log(data);
  if (data.length === 0) {
    return (
      <p className="text-center mt-4 text-accent">Бронирования не найдены.</p>
    );
  }
  return (
    <div className="flex flex-col gap-4 max-h-[calc(100vh-290px)] overflow-y-scroll">
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
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              handleResourceClick={handleResourceClick}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
