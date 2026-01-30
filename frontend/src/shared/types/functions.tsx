import type { DateString } from "./types";

/* eslint-disable react-refresh/only-export-components */
export function firstBigLetter(string: string | undefined): string {
  if (!string) return ''; // Обработка пустой строки
  return string.charAt(0).toUpperCase() + string.slice(1);
}
export function getDaysInMonth(year: number, month: number) {
  const date = new Date(year, month, 1);
  const days = [];

  const firstDayOfWeek = date.getDay();

  const offset = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

  for (let i = 0; i < offset; i++) {
    days.push(null);
  }

  while (date.getMonth() === month) {
    days.push(date.getDate());
    date.setDate(date.getDate() + 1);
  }
  return days;
}
export const GetDD_MM_YYYY = (datestr: string): DateString => {
  const date = new Date(datestr);
  const day = Number(date.getUTCDate().toString().padStart(2, "0"));
  const month = Number((date.getUTCMonth() + 1).toString().padStart(2, "0"));
  const year = Number(date.getUTCFullYear().toString());
  const date_str: DateString = `${year}-${month}-${day}`
  return date_str
}
// export default { getDaysInMonth, firstBigLetter };
