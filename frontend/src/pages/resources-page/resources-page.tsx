import { AnimatePresence, motion } from 'framer-motion';
import ResourcesScreen from '@/features/resources/resource-screen';
// import type { BookingItem } from '@/shared/types/types';
const pageVariants = {
  initial: { opacity: 0, x: 0 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 0 },
};
// interface ResourcesProps {
//   handleResourceClick: (data: BookingItem | undefined) => void
// }

export default function Resources() {
  return (
    <>
      <AnimatePresence mode="wait">
        <motion.div
          // key={selectedResource ? 'details' : activeTab}
          initial="initial"
          animate="animate"
          exit="exit"
          variants={pageVariants}
          transition={{ duration: 0.2 }}
        >
          <ResourcesScreen />
        </motion.div>
      </AnimatePresence>
    </>
  );
}
