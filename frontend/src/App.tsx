// import Button from "./components/small/button/button";
// import Input from "./components/small/input/input";
// import TagButton from "./components/small/tags/tags";
import { MainPage } from "./views/main-page/main-page.tsx";
import { BookingProvider } from "./components/containers/bookingContext/bookingContext.tsx";
function App() {
  window.Telegram?.WebApp?.ready();

  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  // const theme = window.Telegram?.WebApp?.themeParams;

  // Используем цвета из темы Telegram
  // const bgColor = theme?.bg_color || "#0a0a0a";
  // const textColor = theme?.text_color || "#ffffff";
  // const buttonColor = theme?.button_color || "#3b82f6";
  // const linkColor = theme?.link_color || "#06b6d4";
  // const hintColor = theme?.hint_color || "#6b7280";

  // Закоментить строки ниже для тестов визуальной части в браузере
  // Параметры из тг там не появятся!
  if (!user) {
    // return (
    //   <div
    //     style={{
    //       backgroundColor: bgColor,
    //       color: textColor,
    //       minHeight: "100vh",
    //     }}
    //     className="p-4 flex items-center justify-center"
    //   >
    //     <Input
    //       id="v1"
    //       variant="default"
    //       placeholder="penisis"
    //       onChange={() => {}}
    //       span="TEXT"
    //       label="TEXT"
    //     ></Input>
    //     <Input
    //       id="v2"
    //       variant="error"
    //       label="TEXT"
    //       placeholder="TEXT"
    //       onChange={() => {}}
    //       span="TEXT"
    //       isFloating
    //     ></Input>
    //     <Input
    //       id="v3"
    //       variant="success"
    //       label="TEXT"
    //       placeholder="TEXT"
    //       onChange={() => {}}
    //       span="TEXT"
    //       isFloating
    //     ></Input>
    //     {/* <Button
    //       label="Загрузка или приложение открыто не в Telegram..."
    //       size="lg"
    //       variant="error"
    //       onClick={function (): void {
    //         throw new Error("Function not implemented.");
    //       }}
    //     ></Button>
    //     <Button
    //       label="Загрузка или приложение открыто не в Telegram..."
    //       size="md"
    //       variant="error"
    //       onClick={function (): void {
    //         throw new Error("Function not implemented.");
    //       }}
    //     ></Button>
    //     <Button
    //       label="Загрузка или приложение открыто не в Telegram..."
    //       size="xs"
    //       variant="error"
    //       onClick={function (): void {
    //         throw new Error("Function not implemented.");
    //       }}
    //     ></Button> */}
    //   </div>
    // );
    return <BookingProvider>{<MainPage />}</BookingProvider>;
  }
  // Коментировать до этой строчки!
  // Далее идет код страницы
  return <BookingProvider>{<MainPage />}</BookingProvider>;
  // return (
  //   <>
  //     <div
  //       style={{
  //         backgroundColor: bgColor,
  //         color: textColor,
  //         // minWidth:"100vw",
  //         minHeight: "100vh",
  //       }}
  //       className="p-4 flex items-center justify-center"
  //     >
  //       <div className="relative max-w-md w-full">
  //         {/* Анимированная подсветка */}
  //         <div
  //           className="absolute inset-0 rounded-2xl blur-xl animate-pulse"
  //           style={{ backgroundColor: `${buttonColor}20` }}
  //         ></div>

  //         {/* Основная карточка */}
  //         <div
  //           className="relative backdrop-blur-sm rounded-2xl p-6 shadow-2xl border"
  //           style={{
  //             backgroundColor: `${bgColor}cc`,
  //             borderColor: `${linkColor}50`,
  //           }}
  //         >
  //           {/* Статус */}
  //           <div className="flex items-center justify-between mb-6">
  //             <div className="flex items-center gap-3">
  //               <div
  //                 className="w-3 h-3 rounded-full animate-pulse"
  //                 style={{
  //                   backgroundColor: linkColor,
  //                   boxShadow: `0 0 10px ${linkColor}50`,
  //                 }}
  //               ></div>
  //               <span
  //                 className="text-sm font-mono tracking-wider"
  //                 style={{ color: linkColor }}
  //               >
  //                 ONLINE
  //               </span>
  //             </div>
  //             {user?.is_premium && (
  //               <div
  //                 className="px-3 py-1 rounded-full text-xs font-bold tracking-wide"
  //                 style={{
  //                   backgroundColor: buttonColor,
  //                   color: theme?.button_text_color || "#fff",
  //                 }}
  //               >
  //                 ⭐ PREMIUM
  //               </div>
  //             )}
  //           </div>

  //           {/* Аватар */}
  //           <div className="flex justify-center mb-6">
  //             <div className="relative">
  //               <div
  //                 className="w-20 h-20 rounded-full flex items-center justify-center shadow-lg"
  //                 style={{
  //                   background: `linear-gradient(135deg, ${linkColor}, ${buttonColor})`,
  //                   boxShadow: `0 10px 30px ${linkColor}30`,
  //                 }}
  //               >
  //                 <span className="text-2xl font-bold text-white">
  //                   {user?.first_name?.charAt(0).toUpperCase() || "?"}
  //                 </span>
  //               </div>
  //               <div
  //                 className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full border-2 animate-pulse"
  //                 style={{ backgroundColor: linkColor, borderColor: bgColor }}
  //               ></div>
  //             </div>
  //           </div>

  //           {/* Информация */}
  //           <div className="space-y-3">
  //             {[
  //               {
  //                 label: "NAME",
  //                 value: `${user?.first_name || "Unknown"} ${
  //                   user?.last_name || ""
  //                 }`,
  //               },
  //               {
  //                 label: "USERNAME",
  //                 value: `@${user?.username || "anonymous"}`,
  //               },
  //               { label: "USER ID", value: `#${user?.id || "000000"}` },
  //               user?.language_code
  //                 ? {
  //                     label: "LANGUAGE",
  //                     value: user.language_code.toUpperCase(),
  //                   }
  //                 : null,
  //             ]
  //               .filter(
  //                 (item): item is { label: string; value: string } =>
  //                   item !== null,
  //               )
  //               .map((item, i) => (
  //                 <div
  //                   key={i}
  //                   className="rounded-lg p-3 border"
  //                   style={{
  //                     backgroundColor: `${bgColor}80`,
  //                     borderColor: `${hintColor}30`,
  //                   }}
  //                 >
  //                   <div className="flex justify-between items-center">
  //                     <span
  //                       className="text-sm font-mono"
  //                       style={{ color: hintColor }}
  //                     >
  //                       {item.label}
  //                     </span>
  //                     <span
  //                       className="font-semibold"
  //                       style={{ color: i % 2 ? linkColor : buttonColor }}
  //                     >
  //                       {item.value}
  //                     </span>
  //                   </div>
  //                 </div>
  //               ))}
  //           </div>

  //           {/* Статус бар */}
  //           <div
  //             className="mt-6 pt-4 border-t flex items-center justify-between text-xs"
  //             style={{ borderColor: `${hintColor}30` }}
  //           >
  //             <div className="flex items-center gap-2">
  //               <div
  //                 className="w-2 h-2 rounded-full animate-pulse"
  //                 style={{ backgroundColor: buttonColor }}
  //               ></div>
  //               <span className="font-mono" style={{ color: hintColor }}>
  //                 TELEGRAM WEB APP
  //               </span>
  //             </div>
  //             <span className="font-mono" style={{ color: hintColor }}>
  //               v1.0.0
  //             </span>
  //           </div>
  //         </div>
  //       </div>
  //     </div>
  //   </>
  // );
}
export default App;
