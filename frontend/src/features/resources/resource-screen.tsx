import { useEffect, useState } from 'react';
import ResourceMain from './components/resource-main';
import ResourceDetails from './components/resource-details';
import type { DateString, ResourceItem, ResourceTabs } from '@/shared/types/types';
import { GetDD_MM_YYYY } from '@/shared/types/functions';
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
  useEffect(() => { });
  const handleBackClick = () => {
    setResourceActiveTab('main');
  };
  const currentDateUTC = new Date();
  const toISOString = currentDateUTC.toISOString();
  console.log("Сегодня:", GetDD_MM_YYYY(toISOString));
  const [selectedDate, setSelectedDate] = useState<DateString>('0000-00-00');

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
          selectedDate={selectedDate}
          setSelectedDate={setSelectedDate}
        />
      ) : (
        ''
      )}
    </>
  );
}
