import { useEffect, useState } from 'react';
import ResourceMain from './components/resource-main';
import ResourceDetails from './components/resource-details';
import type { BookingItem, Tabs } from '@/shared/types/types';

export default function ResourcesScreen() {
  const [activeTab, setActiveTab] = useState<Tabs>('main');
  const [data, setData] = useState<Array<BookingItem | undefined>>([]);
  const [selectedResource, setSelectedResource] = useState<
    BookingItem | undefined
  >(undefined);
  const handleResourceClick = (resource: BookingItem) => {
    setActiveTab('details');
    setSelectedResource(resource);
    setData(resource);
    // console.log(resource)
  };
  // console.log(data)
  useEffect(() => { });
  const handleBackClick = () => {
    setActiveTab('main');
  };
  return (
    <>
      {activeTab == 'main' ? (
        <ResourceMain
          setActiveTab={setActiveTab}
          activeTab={activeTab}
          handleResourceClick={handleResourceClick}
        />
      ) : activeTab == 'details' ? (
        <ResourceDetails
          data={selectedResource}
          handleBackClick={handleBackClick}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          handleResourceClick={handleResourceClick}
        />
      ) : (
        ''
      )}
    </>
  );
}
