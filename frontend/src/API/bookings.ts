import api from './axiosInstance';
import type { GetAllBookingsResponse } from '../types/bookingContext';

/**
 * GET /api/bookings/all
 * Requires Bearer token (auto-attached from localStorage or setAuthToken())
 */
export async function getAllBookings(): Promise<GetAllBookingsResponse> {
  const res = await api.get<GetAllBookingsResponse>('api/bookings/all', {
    headers: {
      Authorization: 'Bearer AZurPmBtfk6yU3lZ_Omf9A',
    },
  });
  return res.data;
}

export default { getAllBookings };
