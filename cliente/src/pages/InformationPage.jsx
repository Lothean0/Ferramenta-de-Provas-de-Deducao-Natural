import Header from "../components/Header";
import Info from "../components/Info";
import SegmentedControl from "../components/SegmentedControl";
import { useMemo, useState } from "react";
import { translations } from "../utils/translations";


const InformationPage = () => {

  const [language, setLanguage] = useState('PT');
  const t = useMemo(() => (key) => translations[language][key], [language]);

  const handleLanguageToggle = (selectedLanguage) => {
    setLanguage(selectedLanguage);
  };

  return (
    <>
      <Header />
      <SegmentedControl
        onChange={handleLanguageToggle}
      />
      <Info t={t}/>
    </>
  );
};

export default InformationPage;