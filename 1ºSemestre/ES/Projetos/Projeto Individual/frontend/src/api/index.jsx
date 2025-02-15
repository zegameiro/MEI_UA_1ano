import axios from 'axios'

export const api_link = import.meta.env.VITE_API_URL;

export default axios.create({
    baseURL: api_link,
})