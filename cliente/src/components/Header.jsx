import '../styles/Header.css';

function Header({translate}) {
    const t = translate 
    return (
        <header className="header-container">
            <h1 className="title"> 
                {t("title")}
            </h1>
        </header>  
    )
  }
  
  export default Header;
  