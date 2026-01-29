import CalendarScreen from '@/features/calendar/calendar-screen';
import { AnimatePresence, motion } from 'framer-motion';
import { pageVariants } from '@/shared/types/constants';
export default function Calendar() {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        // key={selectedResource ? 'details' : activeTab}
        initial="initial"
        animate="animate"
        exit="exit"
        variants={pageVariants}
        transition={{ duration: 0.2 }}
      >
        <CalendarScreen />;
      </motion.div>
    </AnimatePresence>
  );
  return;
}
