import { useEffect } from 'react';
import ResourceMain from './components/resource-main';
import ResourceDetails from './components/resource-details';
import type { ResourceItem, ResourceTabs } from '@/shared/types/types';
interface ResourcesScreenProps {
  handleResourceClick: (resource: ResourceItem | undefined) => void;
  selectedResource: ResourceItem | undefined;
  setSelectedResource: React.Dispatch<
    React.SetStateAction<ResourceItem | undefined>
  >;
  setResourceActiveTab: React.Dispatch<React.SetStateAction<ResourceTabs>>;
  activeResourceTab: ResourceTabs | undefined;
}
export default function ResourcesScreen({
  handleResourceClick,
  selectedResource,
  setResourceActiveTab,
  activeResourceTab,
}: ResourcesScreenProps) {
  useEffect(() => {});
  const handleBackClick = () => {
    setResourceActiveTab('main');
  };
  return (
    <>
      {activeResourceTab == 'main' ? (
        <ResourceMain
          setResourceActiveTab={setResourceActiveTab}
          activeResourceTab={activeResourceTab}
          handleResourceClick={handleResourceClick}
        />
      ) : activeResourceTab == 'details' ? (
        <ResourceDetails
          data={selectedResource}
          handleBackClick={handleBackClick}
          activeResourceTab={activeResourceTab}
          setResourceActiveTab={setResourceActiveTab}
          handleResourceClick={handleResourceClick}
          selectedDate={''}
        />
      ) : (
        ''
      )}
    </>
  );
}
