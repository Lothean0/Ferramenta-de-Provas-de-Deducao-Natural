import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';

import HomePage from './pages/HomePage';
import PropositionalLogic from './pages/PropositionalLogic'
import TruthTable from './pages/TruthTable';
import QuantificationalLogic from './pages/QuantificationalLogic';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path='/' element={<HomePage />} />
        <Route path='/Propositional-Logic' element={<PropositionalLogic />} />
        <Route path='/Truth-Table' element={<TruthTable />} />
        <Route path='/Quantificational-Logic' element={<QuantificationalLogic />} />
      </Routes>
    </Router>
  </StrictMode>,
)

