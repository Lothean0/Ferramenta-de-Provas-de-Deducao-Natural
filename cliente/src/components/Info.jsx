import { useMemo, useState} from 'react';
import { translations } from '../utils/translations';

import landscape1 from '../assets/img/landscape-1.png';
import ImageWithTooltip from './ImageWithTooltip';

import '../styles/Info.css'; 

function Info() {

    const [language, setLanguage] = useState('PT');
    const t = useMemo(() => (key) => translations[language][key] || key);
    
    return (
        <div className='information-container'>
                                
            <p className='information'>{t("about_propositional_logic")}</p>
                            
            <h2 className='sub-tittle'>{t("input_syntax")}</h2>

            <p className='information'>{t("about_input_syntax")}</p>

            <h2 className='sub-tittle'>{t("suported_rules")}</h2>

                                
            <div className='rules__container'
                style={{ 
                    gap: '2rem',
                    rowGap: '3.5rem',
                    marginLeft: '50px',
                    marginRight: '70px',
                    marginTop: '420px',

                    fontFamily: "'GochiHand', sans-serif",
                    position: 'absolute',
                    background: 'transparent'
                }}
            >
                                
            <ImageWithTooltip
                src={landscape1} 
                alt={"Regras"}
            />
                                
        </div>

        <div className='white-space'/>                
                            
    </div>
  )
}

export default Info
