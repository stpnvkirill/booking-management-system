import ProfileScreen from '@/features/profile/profile-screen';
import { AnimatePresence, motion } from 'framer-motion';
import { pageVariants } from '@/shared/types/constants';
export default function Profile() {
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
        <ProfileScreen />;
      </motion.div>
    </AnimatePresence>
  )
}
