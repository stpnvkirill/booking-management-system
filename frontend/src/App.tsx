import { AuthContainer } from '@/features/auth/auth.tsx';

import Resources from '@/pages/resources-page/resources-page';

import Navbar from '@/features/navbar/navbar';
import { useState } from 'react';
import Calendar from '@/pages/calendar-page/calendar-page';
import Profile from '@/pages/profile-page/profile-page';
// import axios from 'axios';
import { Spinner } from '@/shared/components/spinner/spinner';
import Header from '@/shared/components/header/header';
import Button from '@/shared/components/button/button';
import type { ResourceItem, ResourceTabs } from './shared/types/types';
import { firstBigLetter } from '@/shared/types/functions';
// const useAuth = () => {
// 	const [isAuth, setIsAuth] = useState(true);
// 	const signIn = async (initData?: string | object) => {
// 		const { data } = await axios.post<boolean>(
// 			'https://example.com/auth/signin', // URL эндпоинта аутентификации
// 			{ initData }, // Передаем данные для входа
// 		);
// 		setIsAuth(data); // Устанавливаем статус аутентификации
// 	};
// 	return { isAuth, signIn };
// };

export default function App() {
  window.Telegram?.WebApp?.ready();
  type Tabs = 'resources' | 'calendar' | 'profile';
  const user: boolean = true;
  const isAuthenticated: boolean = true;
  const [activeTab, setActiveTab] = useState<Tabs>('resources');
  // const { isAuth, signIn } = useAuth();
  const isAuth = true;
  // useEffect(() => {
  // 	signIn(window?.Telegram?.WebApp?.initDataUnsafe?.user);
  // }, [signIn]);
  const [selectedResource, setSelectedResource] = useState<
    ResourceItem | undefined
  >(undefined);
  const [data, setData] = useState<ResourceItem>();
  const [activeResourceTab, setResourceActiveTab] =
    useState<ResourceTabs>('main');
  // const user = window.Telegram?.WebApp?.initDataUnsafe?.user; //
  const TG_APP = window.Telegram?.WebApp;

  if (!user) {
    if (isAuthenticated) {
      return (
        <div className="fixed inset-0 z-9999 flex flex-col items-center justify-center bg-neutral-content">
          <Spinner />
          <AuthContainer />
          <Spinner />
        </div>
      );
    }
    return (
      <div className="bg-neutral-content text-center text-neutral p-4 flex items-center justify-center h-dvh">
        Загрузка или приложение открыто не в Telegram...
      </div>
    );
  }
  if (isAuth) {
    const handleBackClick = (): void => {
      setResourceActiveTab('main');
    };
    const handleResourceClick = (resource: ResourceItem | undefined) => {
      setResourceActiveTab('details');
      setSelectedResource(resource);
      setData(resource);
    };
    console.log('App.tsx[80]:', data);
    return (
      // h-screen 
      <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans p-4">
        {activeTab == 'resources' ? (
          <>
            {activeResourceTab === 'main' ? (
              <Header title={import.meta.env.VITE_APP_NAME} subtitle="Ресурсы" children={null} />
            ) : activeResourceTab === 'details' ? (
              <Header
                title={`${data?.name}`}
                subtitle={`${firstBigLetter(data?.location)} • ${firstBigLetter(data?.resource_type)} • ${firstBigLetter(data?.description)}`}
                children={
                  <Button
                    variant="primary"
                    size="xl"
                    width="responsive"
                    shape="text"
                    onClick={handleBackClick}
                    label="←"
                  />
                }
              />
            ) : (
              ''
            )}
            <Resources
              handleResourceClick={handleResourceClick}
              selectedResource={selectedResource}
              setSelectedResource={setSelectedResource}
              activeResourceTab={activeResourceTab}
              setResourceActiveTab={setResourceActiveTab}
            />
          </>
        ) : activeTab == 'calendar' ? (
          <>
            <Header
              title="Календарь"
              subtitle="Расписание бронирований"
              children={null}
            />
            <Calendar />
          </>
        ) : activeTab == 'profile' ? (
          <>
            <Header title="Профиль" subtitle="Ваши бронирования">
              <Button
                label={'Выйти'}
                shape="outline"
                variant="error"
                size="xl"
                width="full"
                onClick={() => {
                  TG_APP?.close();
                }}
              />
            </Header>
            <Profile />
          </>
        ) : (
          ''
        )}
        <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>
    );
  } else {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-neutral-content">
        <Spinner />
      </div>
    );
  }
}
