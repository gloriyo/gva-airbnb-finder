import { DB_URL } from '../config';

// to-do move to server side?

// likely will never need to be used
export function getAllListings() {
  return axios.get(DB_URL);
}

// get specific listing based on params
export function getListing(params) {
    const { id } = params;
  return axios.get(`${DB_URL}/${id}`)
}

