import { useMemo, useState } from "react";

import Header from "../components/Header";
import Home from "../components/Home";

import { translations } from "../utils/translations";

const HomePage = () => {
  const [language, setLanguage] = useState('PT');
  
  const t = useMemo(() => (key) => translations[language][key], [language]);

  const handleLanguageToggle = (selectedLanguage) => {
    setLanguage(selectedLanguage);
  };

  return (
    <>
        <Header translate={t} />
        <Home/>
    </>
    );
};
  
export default HomePage;
  

