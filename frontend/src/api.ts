import axios from 'axios'


export const api = axios.create({
    baseURL: '/api', // nginx proxy → api:8000
})


export type Coin = {
    id: number
    coingecko_id: string
    symbol: string
    name: string
    image_url?: string
    market_cap_rank?: number
    market_cap?: number
    current_price?: number
    created_at: string
    updated_at: string
    meta?: Record<string, unknown>
}