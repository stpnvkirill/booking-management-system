import { AnimatePresence, motion } from 'framer-motion';
import ResourcesScreen from '@/features/resources/resource-screen';
import { pageVariants } from '@/shared/types/constants';
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
