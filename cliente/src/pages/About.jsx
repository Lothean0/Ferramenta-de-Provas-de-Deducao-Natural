import React from "react";
import Header from "../components/Header";
import AboutBody from "../components/AboutBody";


import SegmentedControl from "../components/SegmentedControl";
import { useMemo, useState } from "react";
import { translations } from "../utils/translations";

const About = () => {

  const [language, setLanguage] = useState('PT');
  const t = useMemo(() => (key) => translations[language][key], [language]);

  const handleLanguageToggle = (selectedLanguage) => {
    setLanguage(selectedLanguage);
  };

  return (
    <>
      <Header translate={t}/>
      <SegmentedControl
        onChange={handleLanguageToggle}
      />
      <AboutBody translate={t}/>
    </>
  );
};

export default About;
