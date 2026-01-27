import { AnimatePresence, motion } from 'framer-motion';
import ResourcesScreen from '@/features/resources/resource-screen';
const pageVariants = {
  initial: { opacity: 0, x: 0 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 0 },
};

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
