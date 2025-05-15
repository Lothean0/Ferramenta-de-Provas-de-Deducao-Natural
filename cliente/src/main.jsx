import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';

import HomePage from './pages/HomePage';
import PropositionalLogic from './pages/PropositionalLogic'
import InformationPage from './pages/InformationPage';
import About from './pages/About';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path='/' element={<HomePage />} />
        <Route path='/Propositional-Logic' element={<PropositionalLogic />} />
        <Route path='/Info/Propositional-Logic' element={<InformationPage />} />
        <Route path='/About' element={<About />} />
      </Routes>
    </Router>
  </StrictMode>
)

