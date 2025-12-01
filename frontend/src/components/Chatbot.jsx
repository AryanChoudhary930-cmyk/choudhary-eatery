import { useEffect, useRef, useState } from 'react';

const Chatbot = () => {
  const chatbotRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Check if the Dialogflow messenger is already loaded
    const checkDialogflowLoaded = () => {
      if (customElements.get('df-messenger')) {
        setIsLoaded(true);
        return true;
      }
      return false;
    };

    // If already loaded, set the state
    if (checkDialogflowLoaded()) {
      return;
    }

    // Otherwise, wait for the custom element to be defined
    const waitForDialogflow = setInterval(() => {
      if (checkDialogflowLoaded()) {
        clearInterval(waitForDialogflow);
      }
    }, 100);

    // Cleanup interval on unmount
    return () => clearInterval(waitForDialogflow);
  }, []);

  useEffect(() => {
    // Create and append the chatbot element after the script is loaded
    if (isLoaded && chatbotRef.current && !chatbotRef.current.hasChildNodes()) {
      const dfMessenger = document.createElement('df-messenger');
      dfMessenger.setAttribute('intent', 'WELCOME');
      dfMessenger.setAttribute('chat-title', 'TejasBot');
      dfMessenger.setAttribute('agent-id', '66263d00-e18a-408c-b312-077ca5e914d8');
      dfMessenger.setAttribute('language-code', 'en');
      
      chatbotRef.current.appendChild(dfMessenger);
    }
  }, [isLoaded]);

  return <div ref={chatbotRef}></div>;
};

export default Chatbot;
