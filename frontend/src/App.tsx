// import Button from "./components/small/button/button";
// import Input from "./components/small/input/input";
// import TagButton from "./components/small/tags/tags";
import { MainPage } from './views/main-page/main-page.tsx';
import { BookingProvider } from './types/bookingContext.tsx';
function App() {
  window.Telegram?.WebApp?.ready();
  // Закоментить строки ниже для тестов визуальной части в браузере
  // Параметры из тг там не появятся!

  // const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  // const theme = window.Telegram?.WebApp?.themeParams;

  // Используем цвета из темы Telegram
  // const bgColor = theme?.bg_color || "#0a0a0a";
  // const textColor = theme?.text_color || "#ffffff";
  // const buttonColor = theme?.button_color || "#3b82f6";
  // const linkColor = theme?.link_color || "#06b6d4";
  // const hintColor = theme?.hint_color || "#6b7280";

  // if (!user) {
  //   return (
  //     <div className={`bg-neutral-content text-neutral p-4 flex items-center justify-center h-dvh`}>
  //       Загрузка или приложение открыто не в Telegram...
  //     </div>
  //   );
  // }
  // Коментировать до этой строчки!
  // Далее идет код страницы
  return <BookingProvider>{<MainPage />}</BookingProvider>;
}
export default App;
