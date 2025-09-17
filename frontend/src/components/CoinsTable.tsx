import * as React from 'react'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { Box, Button, Stack, Avatar } from '@mui/material'
import { api, Coin } from '../api'


export default function CoinsTable(){
    const [rows, setRows] = React.useState<Coin[]>([])
    const [loading, setLoading] = React.useState(false)

    const load = React.useCallback(async ()=>{
        setLoading(true)
        try{ const {data} = await api.get<Coin[]>('/coins/'); setRows(data) } finally { setLoading(false) }
    },[])


    React.useEffect(()=>{ load() },[load])

    const refresh = async (id:number)=>{ await api.post(`/coins/${id}/refresh`); await load() }
    const remove = async (id:number)=>{ await api.delete(`/coins/${id}`); await load() }
    const refreshAll = async ()=>{ await api.post(`/coins/refresh-all`); await load() }


    const cols: GridColDef[] = [
        { field: 'id', headerName: 'ID', width: 70 },
        { field: 'image_url', headerName: '', width: 60, renderCell: p => p.value ? <Avatar src={p.value} /> : null },
        { field: 'symbol', headerName: 'Symbol', width: 100 },
        { field: 'name', headerName: 'Název', flex: 1 },
        { field: 'current_price', headerName: 'Cena (USD)', width: 150, valueFormatter: p => p.value != null ? `$${p.value}` : '' },
        { field: 'market_cap_rank', headerName: 'Rank', width: 100 },
        { field: 'actions', headerName: 'Akce', width: 260, renderCell: (p)=> (
        <Stack direction="row" spacing={1}>
            <Button size="small" onClick={()=>refresh(Number(p.id))}>Refresh</Button>
            <Button size="small" color="error" onClick={()=>remove(Number(p.id))}>Smazat</Button>
        </Stack>
    )},
]


return (
    <Box>
        <Stack direction="row" spacing={2} sx={{mb:2}}>
            <Button variant="contained" onClick={refreshAll}>Refresh všech</Button>
            <Button variant="outlined" onClick={load}>Znovu načíst</Button>
        </Stack>
        <div style={{ height: 520, width: '100%' }}>
            <DataGrid rows={rows} columns={cols} loading={loading} getRowId={(r)=>r.id} />
        </div>
    </Box>
    )
}