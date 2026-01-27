// import { MainPage } from './views/main-page/main-page.tsx';
// import { BookingProvider } from './types/bookingContext.tsx';
import BookingsList from './components/BookingsList.tsx';
function App() {
  window.Telegram?.WebApp?.ready();
  // const user = window.Telegram?.WebApp?.initDataUnsafe?.user;

  // Закоментить строки ниже для тестов визуальной части в браузере
  // Параметры из тг там не появятся!
  // if (!user) {
  //   return (
  //     <div className={`bg-neutral-content text-neutral p-4 flex items-center justify-center h-dvh`}>
  //       Загрузка или приложение открыто не в Telegram...
  //     </div>
  //   );
  // }
  // Коментировать до этой строчки!
  // Далее идет код страницы
  // return <BookingProvider>{<MainPage />}</BookingProvider>;
  return <BookingsList />;
}
export default App;
