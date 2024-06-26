import React, { useState, useEffect } from 'react';
import MainComponent from './components/MainComponent';
import WelcomeModal from './components/WelcomeModal';

function App() {
  const [modalIsOpen, setModalIsOpen] = useState(false);

  useEffect(() => {
    setModalIsOpen(true);
  }, []);

  const closeModal = () => {
    setModalIsOpen(false);
  };

  const openModal = () => {
    setModalIsOpen(true);
  };


  return (
    <div className="App">
      <WelcomeModal isOpen={modalIsOpen} onRequestClose={closeModal} />
      <MainComponent openModal={openModal} />
    </div>
  );
}

export default App;
