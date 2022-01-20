// import { DB_URL } from '../config';

// // to-do move to server side?

// // likely will never need to be used
// export function getAllListings() {
//   return axios.get(DB_URL);
// }

// // get specific listing based on params
// export function getListing(params) {
//     const { id } = params;
//   return axios.get(`${DB_URL}/${id}`)
// }

// import { SERVER_URL } from '../config';




import axios from 'axios';

const SERVER_URL = process.env.SERVER_URL || 'http://localhost:8000';
// SERVER_URL = 'http://localhost:8000';

const API = axios.create({ baseURL: SERVER_URL }); 

export const postSearchInputs = (newSearch) => API.post('/api/search', newSearch);

export const getNeighbourhoods = () => API.get('/api/getNeighbourhoods');

// fetch('/api/getNeighbourhoods', {
//   headers : { 
//     'Content-Type': 'application/json',
//     'Accept': 'application/json'
//   }
// })
// .then(res => res.json())
// .then(neighbourhoodOptions => this.setState({ neighbourhoodOptions: neighbourhoodOptions }))
// console.log('calling express api')