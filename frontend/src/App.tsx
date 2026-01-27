import { AuthContainer } from '@/features/auth/auth.tsx';

import Resources from './pages/resources-page/resources-page';

import Navbar from '@/features/navbar/navbar';
import { useState } from 'react';
import Calendar from './pages/calendar-page/calendar-page';
import Profile from './pages/profile-page/profile-page';
export const App = () => {
  window.Telegram?.WebApp?.ready();
  type Tabs = 'resources' | 'calendar' | 'profile';
  const user: boolean = true;
  const isAuthenticated: boolean = true;
  const [activeTab, setActiveTab] = useState<Tabs>('resources');
  // const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  // Закоментить строки ниже для тестов визуальной части в браузере
  // Параметры из тг там не появятся!
  if (!user) {
    return (
      <div
        className={`bg-neutral-content text-center text-neutral p-4 flex items-center justify-center h-dvh`}
      >
        Загрузка или приложение открыто не в Telegram...
      </div>
    );
  }
  if (!isAuthenticated) {
    return (
      <div className="fixed inset-0 z-9999 flex items-center justify-center bg-neutral-content">
        <AuthContainer />
      </div>
    );
  }
  // Коментировать до этой строчки!
  // Далее идет код страницы
  return (
    <>
      {activeTab == 'resources' ? (
        <Resources />
      ) : activeTab == 'calendar' ? (
        <Calendar />
      ) : activeTab == 'profile' ? (
        <Profile />
      ) : (
        ''
      )}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
    </>
  );
};
