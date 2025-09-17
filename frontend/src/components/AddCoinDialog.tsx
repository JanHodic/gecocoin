import * as React from 'react'
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material'


export default function AddCoinDialog({ open, onClose, onSubmit }: { open: boolean; onClose: () => void; onSubmit: (symbol: string)=>void }){
const [symbol, setSymbol] = React.useState('')
return (
    <Dialog open={open} onClose={onClose} fullWidth>
        <DialogTitle>Přidat kryptoměnu</DialogTitle>
        <DialogContent>
            <TextField autoFocus fullWidth margin="dense" label="Symbol (např. btc)" value={symbol} onChange={e=>setSymbol(e.target.value)} />
        </DialogContent>
        <DialogActions>
            <Button onClick={onClose}>Zavřít</Button>
            <Button variant="contained" onClick={()=>{ onSubmit(symbol); setSymbol(''); }}>Přidat</Button>
        </DialogActions>
    </Dialog>
    )
}