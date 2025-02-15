import { BrowserRouter, Route, Routes } from 'react-router-dom'

import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import LandingPage from './pages/LandingPage'
import Layout from './layout/Layout'
import RequiredAuth from './components/RequiredAuth'

function App() {
  return (
    <>
      <BrowserRouter>

        <Routes>
          
          <Route path='/' element={ <Layout><LandingPage /></Layout> } />
          <Route path='/login' element={ <LoginPage /> } />
        
          <Route element={ <RequiredAuth /> }>
            <Route path='/home' element={ <Layout><HomePage /></Layout> } />
          </Route>

        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
