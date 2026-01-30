import { AnimatePresence, motion } from 'framer-motion';
import ResourcesScreen from '@/features/resources/resource-screen';
import { pageVariants } from '@/shared/types/constants';
import type { ResourceItem, ResourceTabs } from '@/shared/types/types';
interface ResourcesProps {
  handleResourceClick: (resource: ResourceItem | undefined) => void;
  setSelectedResource: React.Dispatch<
    React.SetStateAction<ResourceItem | undefined>
  >;
  selectedResource: ResourceItem | undefined;
  setResourceActiveTab: React.Dispatch<React.SetStateAction<ResourceTabs>>;
  activeResourceTab: ResourceTabs | undefined;
}
export default function Resources({
  handleResourceClick,
  setSelectedResource,
  selectedResource,
  setResourceActiveTab,
  activeResourceTab,
}: ResourcesProps) {
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
          <ResourcesScreen
            handleResourceClick={handleResourceClick}
            setSelectedResource={setSelectedResource}
            selectedResource={selectedResource}
            setResourceActiveTab={setResourceActiveTab}
            activeResourceTab={activeResourceTab}
          />
        </motion.div>
      </AnimatePresence>
    </>
  );
}
