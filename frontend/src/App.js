import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import CVBuilder from './components/CVBuilder/CVBuilder';
import CVPreview from './components/CVPreview/CVPreview';
import CreateCV from './components/CreateCV/CreateCV';
import GlobalStyles from './styles/GlobalStyles';

function App() {
  return (
    <Router>
      <GlobalStyles />
      <div className="App">
        <Routes>
          <Route path="/" element={<CVBuilder />} />
          <Route path="/create-cv" element={<CreateCV />} />
          <Route path="/preview/:cvId" element={<CVPreview />} />
        </Routes>
        <ToastContainer position="top-right" />
      </div>
    </Router>
  );
}

export default App;
