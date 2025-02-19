import React from 'react';
import { Link } from 'react-router-dom';

import '../styles/Card.css';


const Card = ({ image, altText, description, title, link }) => {
    return (
        <article className="card__article">
            <img src={image} alt={altText} className="card__img" />
            <div className="card__data">
                <span className="card__description">{description}</span>
                <h2 className="card__title">{title}</h2>
                <Link to={link} className="card__button">
                Try me!
                </Link>
            </div>
    </article>
    )
}

export default Card;