import * as React from 'react'
import { Container, Typography, Button, Stack, CssBaseline } from '@mui/material'
import AddCoinDialog from './components/AddCoinDialog'
import CoinsTable from './components/CoinsTable'
import { api } from './api'


export default function App(){
    const [open, setOpen] = React.useState(false)
    const add = async (symbol: string)=>{ await api.post('/coins/', {symbol}); setOpen(false) }
return (
        <>
            <CssBaseline />
            <Container maxWidth="lg" sx={{py:4}}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{mb:3}}>
                    <Typography variant="h4">Crypto CRUD</Typography>
                    <Button variant="contained" onClick={()=>setOpen(true)}>Přidat kryptoměnu</Button>
                </Stack>
            <CoinsTable />
            </Container>
            <AddCoinDialog open={open} onClose={()=>setOpen(false)} onSubmit={add} />
        </>
    )
}