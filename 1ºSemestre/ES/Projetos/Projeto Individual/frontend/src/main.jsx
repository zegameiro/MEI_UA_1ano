import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { NextUIProvider } from '@nextui-org/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { CookiesProvider } from 'react-cookie'

import App from './App.jsx'
import './index.css'

const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const queryClient = new QueryClient()

createRoot(document.getElementById('root')).render(
  <GoogleOAuthProvider clientId={clientId} >
    <StrictMode>
      <CookiesProvider>
        <QueryClientProvider client={queryClient}>
          <NextUIProvider>
            <main className='light-theme text-foreground bg-background'>
              <App />
            </main>
          </NextUIProvider>
        </QueryClientProvider>
      </CookiesProvider>
    </StrictMode>
  </GoogleOAuthProvider>,
)
